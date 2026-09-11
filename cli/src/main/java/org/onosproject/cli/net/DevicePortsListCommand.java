/*
 * Copyright 2014-present Open Networking Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.onosproject.cli.net;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.karaf.shell.api.action.Argument;
import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.Completion;
import org.apache.karaf.shell.api.action.Option;
import org.apache.karaf.shell.api.action.lifecycle.Service;
import org.onosproject.net.Device;
import org.onosproject.net.Port;
// === Added: PortNumber import for single-port lookup
import org.onosproject.net.PortNumber;
import org.onosproject.net.device.DeviceService;
import org.onosproject.utils.Comparators;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import static org.onosproject.net.DeviceId.deviceId;

/**
 * Lists all ports or all ports of a device.
 * Strict mode:
 *   - Single-port filter requires: ports <deviceId> -p <port> | --port <port>
 *   - Free-form tokens like "port=11003" are rejected with usage.
 */
@Service
@Command(scope = "onos", name = "ports",
        description = "Lists all ports or all ports of a device")
public class DevicePortsListCommand extends DevicesListCommand {

    private static final String FMT = "  port=%s, state=%s, type=%s, speed=%s %s";

    @Option(name = "-e", aliases = "--enabled", description = "Show only enabled ports",
            required = false, multiValued = false)
    @Completion(DeviceIdCompleter.class)
    private boolean enabled = false;

    @Option(name = "-d", aliases = "--disabled", description = "Show only disabled ports",
            required = false, multiValued = false)
    private boolean disabled = false;

    // === Added: strict single-port filter option
    @Option(name = "-p", aliases = "--port", description = "Filter to a single port number (options must precede the device URI). Example: ports -p 11003 <uri>",
    required = false, multiValued = false)
    private String portFilter;

    @Argument(index = 0, name = "uri", description = "Device ID",
            required = false, multiValued = false)
    @Completion(DeviceIdCompleter.class)
    protected String uri = null;

    @Override
    protected void doExecute() {
        DeviceService service = get(DeviceService.class);

        // === Added: require URI when using -p/--port
        if (portFilter != null && uri == null) {
            error("Port filter requires a device URI.");
            printUsage();
            return;
        }

        if (uri == null) {
            // No URI provided: list all devices and their ports (no single-port filtering here)
            if (portFilter != null) {
                error("Port filter cannot be used without specifying a device URI.");
                printUsage();
                return;
            }
            if (outputJson()) {
                print("%s", jsonPorts(service, getSortedDevices(service)));
            } else {
                for (Device device : getSortedDevices(service)) {
                    printDevice(service, device);
                    printPorts(service, device);
                }
            }
            return;
        }

        Device device = service.getDevice(deviceId(uri));
        if (device == null) {
            error("No such device %s", uri);
            return;
        }

        if (outputJson()) {
            print("%s", jsonPorts(service, new ObjectMapper(), device));
        } else {
            printDevice(service, device);
            printPorts(service, device);
        }
    }

    /**
     * Produces JSON array containing ports of the specified devices.
     *
     * @param service device service
     * @param devices collection of devices
     * @return JSON array
     */
    public JsonNode jsonPorts(DeviceService service, Iterable<Device> devices) {
        ObjectMapper mapper = new ObjectMapper();
        ArrayNode result = mapper.createArrayNode();
        for (Device device : devices) {
            result.add(jsonPorts(service, mapper, device));
        }
        return result;
    }

    /**
     * Produces JSON array containing ports of the specified device.
     *
     * @param service device service
     * @param mapper  object mapper
     * @param device  infrastructure device
     * @return JSON array
     */
    public JsonNode jsonPorts(DeviceService service, ObjectMapper mapper, Device device) {
        ObjectNode result = mapper.createObjectNode();
        ArrayNode ports = mapper.createArrayNode();

        // === Added: strict single-port path when -p/--port is present
        if (portFilter != null) {
            PortNumber pn = safePortNumber(portFilter);
            if (pn == null) {
                error("Invalid port number: %s", portFilter);
                printUsage();
                // keep device context; ports array stays empty
            } else {
                Port port = service.getPort(device.id(), pn);
                if (port != null && isIncluded(port)) {
                    ports.add(portNode(mapper, device, port));
                }
            }
        } else {
            for (Port port : service.getPorts(device.id())) {
                if (isIncluded(port)) {
                    ports.add(portNode(mapper, device, port));
                }
            }
        }

        result.set("device", jsonForEntity(device, Device.class));
        result.set("ports", ports);
        return result;
    }

    // === Added: helper to build a single port JSON node
    private ObjectNode portNode(ObjectMapper mapper, Device device, Port port) {
        return mapper.createObjectNode()
                .put("element", device.id().toString())
                .put("port", port.number().toString())
                .put("isEnabled", port.isEnabled())
                .put("type", port.type().toString().toLowerCase())
                .put("portSpeed", port.portSpeed())
                .set("annotations", annotations(mapper, port.annotations()));
    }

    // Determines if a port should be included in output.
    protected boolean isIncluded(Port port) {
        // status filter only; single-port filter handled explicitly
        return (enabled && port.isEnabled()) ||
               (disabled && !port.isEnabled()) ||
               (!enabled && !disabled);
    }

    protected void printPorts(DeviceService service, Device device) {
        // === Added: strict single-port path when -p/--port is present
        if (portFilter != null) {
            PortNumber pn = safePortNumber(portFilter);
            if (pn == null) {
                error("Invalid port number: %s", portFilter);
                printUsage();
                return;
            }
            Port port = service.getPort(device.id(), pn);
            if (port != null && isIncluded(port)) {
                printPortLine(port);
            }
            return;
        }

        List<Port> ports = new ArrayList<>(service.getPorts(device.id()));
        Collections.sort(ports, Comparators.PORT_COMPARATOR);
        for (Port port : ports) {
            if (!isIncluded(port)) {
                continue;
            }
            printPortLine(port);
        }
    }

    // === Added: formatted single-line printer
    private void printPortLine(Port port) {
        String portName = port.number().toString();
        Object portIsEnabled = port.isEnabled() ? "enabled" : "disabled";
        String portType = port.type().toString().toLowerCase();
        String anns = annotations(port.annotations());
        print(FMT, portName, portIsEnabled, portType, port.portSpeed(), anns);
    }

    // === Added: safe parse helper for PortNumber
    private PortNumber safePortNumber(String s) {
        try {
            return PortNumber.fromString(s);
        } catch (Exception e) {
            return null;
        }
    }

    private void printUsage() {
        print("Usage (options must come before the deviceId):");
        print("  ports [-e|--enabled] [-d|--disabled] [-p|--port <portNumber>] <deviceId>");
        print("Examples:");
        print("  ports netconf:10.100.101.21:2022");
        print("  ports -p 11003 netconf:10.100.101.21:2022");
        print("  ports --port 11003 netconf:10.100.101.21:2022");
    }
}