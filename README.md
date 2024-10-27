## phony
A simple phone logbook based on a Raspberry Pi. When the handset is picked up, a greeting message is played through the speaker and the device immediately begins recording from the microphone. Recordings are ended when the phone is placed back down and saved to the microSD card. To aid setup, when two specific keys are held down on the rotary dialer, the previous recording is played through the speaker.

![](/assets/0_Completed_Project.jpeg)

### Parts Used
1. The [phone](https://www.amazon.ca/Sangyn-Landline-Telephone-Classic-Fashioned/dp/B09SKX9CQC/ref=sr_1_17?crid=1DMLJ459A8TH7&dib=eyJ2IjoiMSJ9.9fL4OK0oCWxUeMJph5Fn2tR1eoebF2xD4tN4QkrSFsm81GsRfA2fRyFY8Zm0RvA76OnauTLXRg2EChW-xdqHTTuqD35pjbozbS72Vdt6_Z8tA7H4BOrtyA9EsOC6MdpNMR-58DNeoBKYpkqLFAE_HD30TUYd3ilLMM1uC8Ab7IQqqIFjFxJJLcy1EQZki6Hh_U6q6fA_Li4oMqLZ5CBadAXQ9kveCUQKdy6ipH6PGX-tOjTcdjCh73snCwKlpjUg4UGMjt2AHO1A_Susn2b-wU6IuhnHu5yd91UO4jr9klE.j2yoKTdMirVZA0ap8vFbA422VCeBMkTBeizehWwpfTs&dib_tag=se&keywords=rotary%2Bphone&qid=1729739786&sprefix=rotary%2Bphone%2Caps%2C106&sr=8-17&th=1)
2. [Raspberry Pi 5 8GB](https://www.pishop.ca/product/raspberry-pi-5-8gb/?src=raspberrypi)
   This is what runs the Python code. Note that this Pi model is overkill for this project. I bought this one so I could reuse it in future projects.
3. [Rasbperry Pi active cooler](https://www.pishop.ca/product/raspberry-pi-active-cooler)
   A little fan the fits onto the Raspberry Pi to keep it cool. Once the Pi is stuffed into the plastic phone, it won't be able to dissipate heat effectively so this provides a bit more headroom.
4. [USB-C Power Adapter](https://www.amazon.ca/gp/product/B0CT2HH7FJ/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
   Note that the Pi requires a 27W USB PD supply. You can use a lower wattage supply but the Pi may throttle itself to keep it from drawing too much power and you'll see warning messages in the Raspberry Pi OS GUI.
5. [128GB microSD card](https://www.amazon.ca/gp/product/B08XQ7R3GC/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1)
   This provides nonvolatile storage for the Raspberry Pi operating system and the audio recordings. This card is also overkill; even 16GB should be plenty of room.
6. [IQaudio Codec Zero](https://www.pishop.ca/product/iqaudio-codec-zero/)
   This board plugs in to the Raspberry Pi to give it an analog micrphone input and an amplified speaker output that will be used to drive the phone handset.
7. [M2.5 hex spacers + screws](https://www.amazon.ca/M2-5-Threaded-Motherboard-Hexagonal-Assortmen/dp/B01N5RDAUX/ref=sr_1_14?crid=1Q2TVLR5G3YGF&dib=eyJ2IjoiMSJ9.9Q7MObpbN4FVcO_-sJARGc_1zYGYEcNhmhN2mwBKoyFEfqXa3CI3jCQmVbZYmzFtztr4Uj0hbV-xrYmNPBTSRg7f2Zps4zEOyatRrWRFCgitN_1hDS80W6bCSoiNOWyUUFpBZHzrbs0PE45hnbI26Pdbq3eMVr4DPLTe7Bsc-NKzkuHlY6pivYZ3ZCvf6FVqjEfR5k_4yrO3A_0gaqGNMxWGxylrMC01SlJ2Ng82YjPfjjyt1BE8mBEzC2lDy20-qJolQpp77vOKGctn6WeOVCQGERXGVC9HXOo8P5zEXac.Azvb0Ht3aZarLWVd9jj-3Os8793ho1bPkGvc0jfQJBs&dib_tag=se&keywords=m2.5+11mm+hex+spacer&qid=1729960220&sprefix=m2+5+11mm+hex+spacer%2Caps%2C73&sr=8-14)
   These are for extending the Codec Zero board away from the Pi since the active cooler will interfere with board and make it not fit.
8. [Pin header extenders](https://www.amazon.ca/GeeekPi-Stacking-Raspberry-Specifications-Extender/dp/B08GC18NMK/ref=sr_1_7?crid=2OXO5TX5Z6U3J&dib=eyJ2IjoiMSJ9.QseeDI_KsJ-dG_l1SRS1MdVtiiWkF8aQj8j9SQXrXY6NNZ6KpprH1L0cICz8eJPf9LA5M2ecM2DN_x-lRpJuSyX9mWRpAayrLzJuXN3ZH-lgPmhAnsEPyI9QIPSK2nUvyUapCwVG-f_pfXuSGqO5vls0bxoSKMOTsoJioJeSnasHUKlGIAob878c4m6z6Rv5JX78wvWwtv_QP_dcpbzZ4MXOy8YfnkJJXzkHtqMUr3rgHsNImrHlJrOUwIXKEqc0RnMwfGla24bSO5PSnguavRh8tzpl6ujdyTe1nCF4n6g.zcwVQmaZZK-Qx4tCcOJJyPOLb_Re0W1_ALje-7S-fHk&dib_tag=se&keywords=raspberry+pi+header&qid=1729960377&sprefix=raspberry+pi+header%2Caps%2C96&sr=8-7)
   These are also used for extending the Codec Zero from the Pi. I ended up using some scrap header I had around and soldering it in place.

### Tools Required
1. Computer with microSD slot
2. Soldering iron
3. Soldering flux and solder
4. Wirestrippers
5. Phillips screwdriver
6. Electrical tape and duct tape
7. Cyanoacrylate glue (Krazy glue). Optional

### Steps
1. Remove the rubber pads on the bottom of the phone to reveal screw holes. Unscrew the base and separate, taking care to open it slowly as there are some wires going from the circuit board inside to a speaker attached to the base.
2. Unscrew the speaker from the base and unscrew the main PCB from the phone body.
3. Note the groups of wires and ribbon cables going to the PCB.
![](/assets/1_Original_Phone_PCB.jpeg)![](/assets/2_Original_Wiring.jpeg)
4. Desolder or neatly cut the two ribbon cables from the PCB.
5. Desolder or neatly cut the group of 4 wires going to the handset jack on the back of the phone.
6. Separate the PCB entirely from the body of the phone and throw it away. Note there will still be wires going from the PCB to the line jack and speaker. I chose to remove the line jack and leave the resulting hole empty on the back of the phone. If you want to keep the line jack, I suggest cutting the wires off close to the jack so they won't interfere with anything.
7. Prepare the hardware...
   - There are 4 wires and two ribbon cables that need to be soldered to the Codec Zero board. The images show where to solder the four wires. The black and yellow wires go to the microphone within the handset, so they get soldered to the electret microphone input on the Codec Zero. The green and red pair go to the handset speaker, so they go to the speaker output on the Codec Zero. Note that you don't have to solder the green and red wires as I did here - you can insert them into the green screw terminal block to achieve the same thing. I chose to cover the wire connections in Krazy glue to make them a bit more robust. I did a truly awful job with the glue.
![](/assets/3_Codec_Zero_Wire_Diagram.jpeg)![](/assets/4_Codec_Zero_with_Wires.jpeg)
    - The image below shows how and where to connect the ribbon cables. The thin ribbon cable is for sensing when the phone handset is picked up and put down. The wide ribbon cable goes to the dialer buttons and allows the Pi to sense when the user has simultaneously pressed in the '#' and 'Redial' buttons, which is used for confirming the phone is working properly. Prepare the ribbon cable with the wire strippers so that only a small length of wire is exposed before soldering to the Codec Zero.
![](/assets/5_Codec_Zero_Ribbon_Cables.jpeg)
    - Install the active cooler on the Pi. It should snap down with the captive spring-loaded push buttons. Plug the fan cable in to the 4-pin fan header next to the USB 2.0 ports.
    - The active cooler unfortunately makes the Codec Zero board not fit on the Pi properly. To get around this, install the hex spacers and a pin header extender as shown. Note that I chose to use some scrap pin header I had lying around and soldered all the pins between them together.
![](/assets/6_Pi_with_Extenders.jpeg)![](/assets/7_Pi_with_Extenders2.jpeg)
    - Install the Codec Zero onto the Pi and use the M2.5 screws to attach them together.
![](/assets/8_Pi_and_Codec_Attached.jpeg)
    - At this point, you're ready to start on the software. I recommend leaving the Pi dangling from the wires for now in case you need to debug an issue later on.
7. Prepare the software...
    - Follow [these](https://www.raspberrypi.com/documentation/com
    puters/getting-started.html) instructions to set up the Pi with the OS. Make sure to set up the WiFi access and enable the VNC server so you can remotely access it as soon as it boots, or otherwise, you'll need to plug in a display + keyboard + mouse. You can optionally install Raspberry Pi Connect if you want to be able to access the Pi over the internet. I used the Imager tool on the same page to prepare the microSD card.
    - Plug the microSD card in and supply power via the USB-C port. It should boot within 30s.
        - If you didn't install Raspberry Pi Connect, get the IP address of your Pi through your home router. Open a connection to your Pi using [TigerVNC](https://tigervnc.org/).
        - If you did install Connect, you also have the option of opening a VNC session to your machine through the [Connect portal](https://connect.raspberrypi.com/sign-in).
    - Clone this Git repo onto the Pi, or alternatively, download it and transfer it over with USB, scp, rsync, etc.
    - Copy the two files from the repo to your Pi's drive:
        - Copy `config.txt` to `/boot/firmware/config.txt`:
            ```
          cp <path to phony repo>/os_cfg/config.txt /boot/firmware/config.txt
            ```
        - Copy `rc.local` to `/etc/rc.local`:
            ```
            cp <path to phony repo>/os_cfg/rc.local /etc/rc.local
            ```
        - Reboot the Pi
    - Once the Pi is back up, reconnect to it and test if things are working by starting the phony script:
      ```
      python <path to phony repo>/phony.py
      ```
      You should see `Program started at...` printed. You may need to install some dependent libraries via pip.
    - With the program running, you can pick up the handset and should be able to hear a greeting message played through the speaker. Try leaving a message and hang up the phone.
    - Pick up the phone again and hold down the '#' and 'Redial' buttons at the same time for a few seconds. You should hear your previous message play back to you.
    - Press Ctrl + C in your terminal window to terminate phony.
    - You can record your own greeting using this command:
      ```
      arecord --device=plughw:1,0 --format=S16_LE --rate=44100 <path to output file>.wav
      ```
      Copy the recorded file to overwite the one in the phony repo:
      ```
      cp <path to output file>.wav <path to phony repo>/greeting.wav
      ```
    - Note that phony will write recordings to `<path to phony repo>/out/`
    - If everything looks good, add the phony script as a cronjob to get it to run automatically each time the Pi boots. Open the editor:
      ```
      crontab -e
      ```
      Add this line to the bottom of the file and save it:
      ```
      @reboot python <path to phony repo>/phony.py &
      ```
      Reboot the Pi.
    - Check once more that the phone is still operational and then unplug the power.
8. Secure the Raspberry Pi into the bottom of the base of the phone. I didn't have time to make anything proper so I just taped it in with duct tape. As a matter of caution, I also covered the bottom of the Pi PCB with electrical tape to make sure the bottom of the PCB wouldn't short on the steel plate in the base.
![](/assets/9_Pi_Insulated_with_Tape.jpeg)![](/assets/10_Pi_Secured_in_Phone_Body.jpeg)
9. Reattach the phone body and base, making sure you have plugged in a USB-C cable into the Pi and routed it out of the back of the phone, before screwing it back together.
