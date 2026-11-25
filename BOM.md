# RoverBuddy X1 – Bill of materials

[Download CSV](bom.csv)

Prices are in USD. Shipping and final costs still need checking.

| Item | Quantity | Unit price (USD) | Total (USD) | Link | Description |
| --- | ---: | ---: | ---: | --- | --- |
| Raspberry Pi 5 4GB kit incl official 27W PSU, active cooler, HDMI lead and case | 1 | 175.81 | 175.81 | [Supplier](https://geeksvalley.com/product/raspberry-pi-5-4gb-kit/) | Runs the camera software and comes with a cooler and desk power supply. |
| SanDisk Extreme A2 microSDXC 64GB SDSQXAH-064G-GN6MN | 1 | 36.83 | 36.83 | [Supplier](https://pcpark.sa/en/collections/flash/products/sandisk-sdsqxah-064g-gn6mn) | Holds the Pi software if this exact card is in stock. |
| Raspberry Pi Pico 2 with Headers (SC1632) | 1 | 6.00 | 6.00 | [Supplier](https://www.digikey.com/en/products/detail/raspberry-pi/SC1632/26241102) | Controls the four motors. |
| USB-A to Micro-B USB 2.0 data cable 0.5 m | 1 | 2.67 | 2.67 | [Supplier](https://ielectrony.com/en/product/micro-usb-cable-0-5m/) | Carries data between the Pi and Pico. |
| Raspberry Pi Camera Module 3, Sony IMX708, standard lens | 1 | 52.00 | 52.00 | [Supplier](https://saudi.microless.com/product/raspberry-pi-camera-module-3-standard-sony-imx708-sensor-11-9mp-resolution-7-4mm-sensor-diagonal-f-1-8-aperture-phase-detection-autofocus-15-x-1mm-fpc-150mm-ribbon-cable-length-sc0872/) | Gives the rover its front view. |
| Raspberry Pi 5 camera cable, Standard-Mini 22-pin to 15-pin, 500mm (Adafruit 5820) | 1 | 2.50 | 2.50 | [Supplier](https://www.adafruit.com/product/5820) | Check this cable through the full head movement. |
| Waveshare 20109 5inch HDMI LCD (H) V4 capacitive USB touch display | 1 | 50.99 | 50.99 | [Supplier](https://www.waveshare.com/product/5inch-hdmi-lcd-h-v4.htm) | Uses HDMI for the picture and USB for touch. |
| Mini external USB stereo speaker for Raspberry Pi greeting audio | 1 | 7.33 | 7.33 | [Supplier](https://ielectrony.com/en/product/mini-external-usb-stereo-speaker/) | Plays greetings from the Pi. |
| Adafruit 3777 TT DC gearbox motor 1:48, 3-6V, supplied 200mm leads | 4 | 2.95 | 11.80 | [Supplier](https://www.adafruit.com/product/3777) | Each wheel gets its own motor. |
| Cytron MDD3A dual brushed DC motor driver, 3A continuous per channel | 2 | 9.30 | 18.60 | [Supplier](https://www.cytron.io/c-dc-motor/c-motor-driver/p-3amp-4v-16v-dc-motor-driver-2-channels) | Each board drives two motors. |
| HC-SR04 ultrasonic obstacle sensor | 1 | 6.13 | 6.13 | [Supplier](https://ielectrony.com/en/product/%D8%AD%D8%B3%D8%A7%D8%B3-%D8%A7%D9%84%D8%AA%D8%B1%D8%A7-%D8%B3%D9%88%D9%86%D9%8A%D9%83-hc-sr04/) | Measures the distance ahead. |
| 1kΩ 1/4W 1% resistor for HC-SR04 ECHO 5V-to-3.3V divider | 1 | 0.13 | 0.13 | [Supplier](https://ielectrony.com/en/product/%D8%B9%D8%AF%D8%AF-1-%D9%85%D9%82%D8%A7%D9%88%D9%85%D8%A9-1k-ohm-1-4w/) | One of two resistors in the proposed echo divider; check before use. |
| 2kΩ 1/4W 1% resistor for HC-SR04 ECHO 5V-to-3.3V divider | 1 | 0.13 | 0.13 | [Supplier](https://ielectrony.com/en/product/%D8%B9%D8%AF%D8%AF-1-%D9%85%D9%82%D8%A7%D9%88%D9%85%D8%A9-2k-ohm-1-4w/) | Pairs with the 1 kΩ resistor in the proposed echo divider. |
| DFRobot FIT0765 black 60mm LEFT mecanum wheel with coupling | 2 | 6.90 | 13.80 | [Supplier](https://www.dfrobot.com/product-2268.html) | Check the left wheels against the maker’s roller diagram. |
| DFRobot FIT0766 black 60mm RIGHT mecanum wheel with coupling | 2 | 6.90 | 13.80 | [Supplier](https://www.dfrobot.com/product-2269.html) | Pairs with the two left wheels. |
| ROBOTIS FR12-H101K XM430 hinge frame and idler bearing (903-0239-000) | 1 | 40.60 | 40.60 | [Supplier](https://en.robotis.com/shop_en/item.php?it_id=903-0239-000) | Check fit and shipping before buying this optional pan bracket. |
| D645MW tilt mounting bracket and custom adapters | 1 | 60.00 | 60.00 | [Supplier](https://www.thanfa.com/en/rfq/) | The $60 is an estimate for two pieces until a supplier quotes them. |
| ROBOTIS DYNAMIXEL XM430-W210-T pan actuator (902-0125-000) | 1 | 269.90 | 269.90 | [Supplier](https://en.robotis.com/shop_en/item.php?it_id=902-0125-000) | Check the pan mount, TTL cable and separate regulated 12 V supply. |
| Hitec D645MW tilt actuator (HCS ordering part 36645S) | 1 | 49.99 | 49.99 | [Supplier](https://www.hiteccs.com/actuators/product-details/D645MW) | Check the tilt mount, horn, 6 V supply and PWM input. |
| Pololu 2184 servo extension cable, 300mm, 22AWG, JR/Futaba male-female | 1 | 4.64 | 4.64 | [Supplier](https://www.pololu.com/product/2184/specs) | Check cable length, polarity, current rating and stock. |
| Hitec R-ML25 25T aluminum horn (55738) if required | 1 | 12.99 | 12.99 | [Supplier](https://hitecrcd.com/25t-aluminum-servo-horn/) | Check which screws come with this optional horn. |
| Venom 15190 preassembled 3S 11.1V 2200mAh 50C LiPo, UNI 2.0 adapter system | 2 | 84.00 | 168.00 | [Supplier](https://hobby-rc.net/product/بطارية-venom-50c-3s-2200mah-11-1v-lipo/) | The planned power boards use this 3S pack. |
| SkyRC S100neo SK-100202 AC/DC balance charger with storage mode | 1 | 116.53 | 116.53 | [Supplier](https://hobbysportzksa.com/en-sa/products/sky-rc-s100neo-ac-dc-charger-item-no-sk-100202) | Have an adult check the battery and charger settings, including storage mode. |
| LiPo battery storage/charging bag, flame-retardant glass-fiber pouch, 10x20cm | 1 | 7.47 | 7.47 | [Supplier](https://www.noon.com/saudi-en/lipo-battery-safe-bag-210d-high-grade-fire-retardant-material-explosion-proof-high-temperature-resistant-lipo-charging-sack-for-drone-rc-battery-storage-charging-workshop-home-protection/Z0A0E59DC389AD5CB1E1BZ/p/) | Use with adult oversight and check the seller’s protection claims. |
| 20cm reusable LiPo retention strap, TWO individual straps | 2 | 2.40 | 4.80 | [Supplier](https://www.pixelelectric.com/drones-parts/drone-assembly-parts/accessories/rc-battery-belt-strap-cable-tie/) | Holds the pack in its tray without squeezing it. |
| Locking emergency-stop push button LAY37, 10A thermal rating (DC rating TBC) | 1 | 2.80 | 2.80 | [Supplier](https://ielectrony.com/en/product/660vac-10a-dpst-emergency-stop-push-button-switch/) | Check the DC rating before using this as the drive stop. |
| DC-rated main power switch matched to measured maximum current | 1 | 2.67 | 2.67 | [Supplier](https://ielectrony.com/en/product/symfonia-ad2212-round-push-button-12v-on-off-power-switch-suitable-for-10a250vac-20a12vdc/) | Check the DC interrupt rating, pack voltage and startup current. |
| RS PRO 237-5266 inline ATO blade fuse holder, 32V, 15A holder, 16AWG leads | 1 | 10.23 | 10.23 | [Supplier](https://sa.rsdelivers.com/product/rs-pro/rs-pro-15-a-in-line-fuse-holder-32-v/2375266?backToResults=1) | Check the listing for the main battery fuse holder. |
| Littelfuse 0287010.PXCN ATOF 10A 32VDC fuse; one installed plus one spare | 2 | 0.35 | 0.70 | [Supplier](https://www.digikey.com/en/products/detail/littelfuse-inc/0287010-PXCN/2519807) | Includes a spare; match the fuse rating to the power system. |
| Yahboom YB-MPP01-V1.0 Pi 5 PD power board, 7-24V input for 5V/5A | 1 | 25.00 | 25.00 | [Supplier](https://geekworm.com/products/yb-mpp01) | Planned USB-C power board for the Pi 5. |
| Pololu 6V 5.5A switching regulator D36V50F6 for D645MW tilt | 1 | 39.95 | 39.95 | [Supplier](https://www.pololu.com/product/4092) | Check load changes and grounding on the 6 V tilt supply. |
| Pololu D36V50F6 6 V regulator, one per motor driver | 2 | 39.95 | 79.90 | [Supplier](https://www.pololu.com/product/4092) | Front and rear motor drivers have separate 6 V supplies. |
| Safa SKU1690 XT60 male/female connector cable pair | 1 | 9.33 | 9.33 | [Supplier](https://www.safaelectronics.com/product/xt60-connector-with-cable-mf) | Match this connector to the actual battery plug. |
| WAGO 221-415 5-way lever connectors, one pack of 10 (use separate + and - nodes) | 1 | 17.79 | 17.79 | [Supplier](https://my.rs-online.com/web/p/standard-terminal-blocks/8837557) | Keep the positive and negative power connections separate. |
| TW21 twin flexible copper PVC cable 2 x 1.0mm2, three one-metre lengths | 3 | 0.33 | 0.99 | [Supplier](https://ielectrony.com/product/%D8%B3%D9%84%D9%83-%D9%85%D8%B2%D8%AF%D9%88%D8%AC-%D9%85%D8%B3%D8%B7%D8%AD-%D9%88%D9%85%D8%B9%D8%B2%D9%88%D9%84-pvc-2x-1-0-mm/) | Check the wire rating against the planned current. |
| Silicone 22AWG flexible signal and motor hookup wire about 2m each color | 1 | 21.07 | 21.07 | [Supplier](https://ielectrony.com/en/product/22awg-6-colors-mix-kit-electrical-wire-copper-wire-for-diy/) | Connects motors and low-current signals. |
| 40 x 20cm male-to-female Dupont jumper wires | 1 | 5.33 | 5.33 | [Supplier](https://ielectrony.com/en/product/%D8%B9%D8%AF%D8%AF-40-%D8%B3%D9%84%D9%83-%D8%B3%D9%84%D9%83-%D8%B0%D9%83%D8%B1-%D8%A7%D9%86%D8%AB%D9%89-20-%D8%B3%D9%85/) | Use for controller signals only. |
| 40 x 20cm female-to-female Dupont jumper wires | 1 | 5.33 | 5.33 | [Supplier](https://ielectrony.com/en/product/%D8%B9%D8%AF%D8%AF-40-%D8%B3%D9%84%D9%83-%D8%A7%D9%86%D8%AB%D9%89-%D8%A7%D9%86%D8%AB%D9%89-20-%D8%B3%D9%85/) | Use for low-current modules and GPIO only. |
| 2pcs insulated 18AWG female spade terminal leads 30cm | 1 | 2.67 | 2.67 | [Supplier](https://ielectrony.com/en/product/6-3mm-female-spade-crimp-terminal-with-insulating-sleeve-and-300mm-red-and-black-wires/) | Check that the switch has matching 6.3 mm tabs. |
| 5x7cm solderable copper prototyping perfboard | 1 | 2.27 | 2.27 | [Supplier](https://ielectrony.com/en/product/57-cm-universal-pcb-board/) | Holds the resistors and signal interface. |
| Heat shrink insulation tubing 4mm x 1m | 1 | 1.20 | 1.20 | [Supplier](https://ielectrony.com/en/product/heat-shrink-tubing-4mm-black-1-meter/) | Covers small solder joints. |
| Heat shrink insulation tubing 8mm x 1m | 1 | 1.87 | 1.87 | [Supplier](https://ielectrony.com/en/product/heat-shrink-tubing-8mm-black-1-meter/) | Covers larger cable joints. |
| Nylon cable ties, 5-piece pack 292 x 3.6mm; TWO packs | 2 | 0.40 | 0.80 | [Supplier](https://ielectrony.com/en/product/nylon-tie-292x3-6mm/) | Keeps wires clear of wheels and gears. |
| TAC Z-BG-F8 open grommet 8mm, four pieces | 4 | 0.07 | 0.28 | [Supplier](https://electrotel.sa/products/tac-grommet-open) | Protects wires where they pass through the body. |
| 200-piece M3/M2.5 brass standoff / nuts / screws robot hardware kit | 1 | 15.07 | 15.07 | [Supplier](https://ielectrony.com/en/product/200pcs-screw-kit-for-robot-accessories/) | Mounts the boards and body. |
| M2x10 camera mounting screws, pack of 5; matching captive nuts INCLUDED in print-service quote request | 1 | 0.27 | 0.27 | [Supplier](https://ielectrony.com/en/product/m2x10-304-stainless-steel-cross-recessed-pan-head-phillips-screws-5pcs/) | Check whether the camera takes M2 or M2.5 screws. |
| M3x20 stainless nonpointed bolts pack of 5 | 1 | 0.31 | 0.31 | [Supplier](https://ielectrony.com/en/product/m3x20-bolt-non-pointed-5pcs/) | Only needed if the printed mounts take 20 mm screws. |
| PETG printing, cleanup, inserts, M2 nuts and screw-down cable guides for final verified CAD parts | 1 | 146.67 | 146.67 | [Supplier](https://omq3d.com/en/pricing.html) | Estimated printing and finishing cost, including inserts and cable guides. |
| UNI-T UT33A+ digital multimeter | 1 | 22.67 | 22.67 | [Supplier](https://ielectrony.com/en/product/digital-multimeter-ut33a/) | Checks voltage, continuity and polarity. |
| NEBCO clear OTG safety glasses, seller claims EN166 | 1 | 1.47 | 1.47 | [Supplier](https://nebcoksa.com/en/otg-safety-glasses/p99230678) | Check the exact listing for eye protection. |
| 30x20cm heat-insulating silicone soldering work mat | 1 | 6.67 | 6.67 | [Supplier](https://ielectrony.com/en/product/heat-insulation-silicone-working-mat-3020cm/) | Optional if there is already a suitable soldering surface. |
| Compact basic 1.5mm/2mm/2.5mm/3mm Allen key set | 1 | 4.00 | 4.00 | [Supplier](https://ielectrony.com/product/%D9%85%D9%81%D8%A7%D8%AA%D9%8A%D8%AD-%D8%B3%D8%AF%D8%A7%D8%B3%D9%8A%D8%A9-%D8%A7%D9%84%D9%8A%D9%86/) | Fits the motor and servo screws. |
| Adjustable 60W soldering kit with iron, stand, solder, wire stripper/cutter, tips, pump, sponge and tweezers | 1 | 26.13 | 26.13 | [Supplier](https://ielectrony.com/en/product/useful-220v-60w-uk-plug-soldering-handy-kit/) | Includes soldering and wire prep tools. |
| ROBOTIS U2D2 USB-to-DYNAMIXEL interface (902-0132-000) | 1 | 32.10 | 32.10 | [Supplier](https://en.robotis.com/shop_en/item.php?it_id=902-0132-000) | Connects the Pi to the pan servo over TTL; check USB cable and separate power. |
| ROBOTIS U2D2 Power Hub Board Set (902-0145-001) | 1 | 19.00 | 19.00 | [Supplier](https://en.robotis.com/shop_en/item.php?it_id=902-0145-001) | Check the cable fit before feeding regulated 12 V to the pan servo. |
| DFRobot DFR0946 adjustable buck-boost module for 12V pan supply - candidate | 1 | 8.90 | 8.90 | [Supplier](https://www.dfrobot.com/product-2539.html) | Check voltage, load, heat, protection and fit before using this pan supply. |
| ROBOTIS X3P 240 mm cable pack (10 pcs, 903-0250-000) if required | 1 | 25.89 | 25.89 | [Supplier](https://www.robotis.ch/488-robot-cable-x3p-240mm-10pcs) | Optional extensions if the included pan cables are too short; check stock and shipping. |
| SN74AHCT125N tilt signal buffer (only if needed) | 1 | 0.95 | 0.95 | [Supplier](https://www.digikey.com/en/products/detail/texas-instruments/SN74AHCT125N/375798) | Check input and startup before choosing this optional tilt buffer. |
| MR106ZZ pivot bearings 6 x 10 x 3 mm (draft candidate) | 2 | 2.80 | 5.60 | [Supplier](https://www.jsumo.com/mr-106-zz-miniature-bearing-6x10x3mm-6mm-hole) | Check bearing fit and delivery to Riyadh. |
| Neck brackets, bearing plates and pivot flange hardware (draft) | 1 | 155.00 | 155.00 | [Supplier](https://www.thanfa.com/en/rfq/) | Get a quote for two brackets, two plates, a shaft, a spacer and a washer. |
| Mounting bolts, nuts and spacers (draft, if not covered by existing kits) | 1 | 35.65 | 35.65 | [Supplier](https://www.noon.com/saudi-en/m2-m3-m4-m5-nuts-and-bolts-assorted-set-1225-pcs-carbon-steel-hex-socket-head-cap-screws-bolts-and-nuts-kit-thread-fastener-machine-hex-bolts-nuts-assortment-kit-with-4pieces-hex-keys-for-free/ZCF1A998446E792981AECZ/p/) | Estimate includes a SAR 114.94 kit and $5 for missing sizes; check existing hardware first. |

**Estimated parts subtotal: $1,869.97 (SAR 7,012.39)**

Prices include estimates. Final quotes, shipping and any additional taxes are still pending. The optional buffer is a price reference.

## Price checks

- iElectrony screw kit: SAR 56.50, already in the BOM. It includes M3 nuts and 6 mm screws, so the longer bolts still need checking.
- Noon screw assortment: SAR 114.94 listed. This is a backup price reference only. It contains many extra pieces and does not cover every exact size.
  https://www.noon.com/saudi-en/ZCF1A998446E792981AECZ/p/
- Custom metal price estimates use published prototype machining ranges: https://yeyuancnc.com/pricing/ . The $155 estimate is two brackets at $35 each, two plates at $15 each, a pivot shaft at $35, and a spacer and washer at $10 each. Actual metal, fit, delivery, and fabrication prices need a supplier quote: https://www.thanfa.com/en/rfq/

## Delivery and quote checks

- Custom metal parts: $215 is an estimate. Request a written quote covering the tilt bracket, adapters, neck brackets and bearing/pivot hardware: https://www.thanfa.com/en/rfq/
- Printing: $146.67 is a budget. The print supplier needs the actual printable part files, material and finishing requirements for a confirmed quote: https://omq3d.com/en/calculator.html
- iElectrony: Saudi delivery is listed as 1–3 business days for major cities; exact cost and timing appear at checkout: https://ielectrony.com/en/shipping-payment-methods/
- Adafruit ships to Saudi Arabia; check the cart for shipping and import fees: https://www.adafruit.com/shipping_locations
- DigiKey delivery charges depend on the order and destination: https://www.digikey.com/en/help-support/delivery-information/international-shipping-rates
- Saudi standard VAT is 15%; check which prices already include VAT before adding any tax: https://zatca.gov.sa/en/RulesRegulations/VAT/Pages/About-VAT.aspx

Final supplier quotes and delivered total are pending. No order has been placed.
