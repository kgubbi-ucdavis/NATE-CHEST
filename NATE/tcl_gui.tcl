namespace eval Test {

    variable ledValue 0
    variable dashboardActive 0
    variable Switch_off 1

    proc toggle { position } {
		set ::Test::ledValue ${position}
        ::Test::updateDashboard
        }
   
    proc sendText {} {
        set sendText [toolkit_get_property sendTextText text]
        toolkit_set_property receiveTextText text $sendText
        }

    proc dashBoard {} {

        if { ${::Test::dashboardActive} == 1 } {
            return -code ok "dashboard already active"
        }

        set ::Test::dashboardActive 1
        #
        # top group widget
        #
        toolkit_add  topGroup group self
        toolkit_set_property  topGroup expandableX false
        toolkit_set_property  topGroup expandableY false
        toolkit_set_property  topGroup itemsPerRow 1
        toolkit_set_property  topGroup title ""

        #
        # leds group widget
        #
        toolkit_add  ledsGroup group topGroup
        toolkit_set_property  ledsGroup expandableX false
        toolkit_set_property  ledsGroup expandableY false
        toolkit_set_property  ledsGroup itemsPerRow 2
        toolkit_set_property  ledsGroup title "LED State"

        #
        # leds widgets
        #
        toolkit_add  led0Button button ledsGroup 
        toolkit_set_property  led0Button enabled true
        toolkit_set_property  led0Button expandableX false
        toolkit_set_property  led0Button expandableY false
        toolkit_set_property  led0Button text "Toggle"
        toolkit_set_property  led0Button onClick {::Test::toggle 1}

        toolkit_add  led0LED led ledsGroup
        toolkit_set_property  led0LED expandableX false
        toolkit_set_property  led0LED expandableY false
        toolkit_set_property  led0LED text "LED 0"
        toolkit_set_property  led0LED color "green_off"

        toolkit_add  led1Button button ledsGroup 
        toolkit_set_property  led1Button enabled true
        toolkit_set_property  led1Button expandableX false
        toolkit_set_property  led1Button expandableY false
        toolkit_set_property  led1Button text "Turn ON"
        toolkit_set_property  led1Button onClick {::Test::toggle 2}

        toolkit_add  led1LED led ledsGroup
        toolkit_set_property  led1LED expandableX false
        toolkit_set_property  led1LED expandableY false
        toolkit_set_property  led1LED text "LED 1"
        toolkit_set_property  led1LED color "green_off"


        #
        # sendText widgets
        #
        toolkit_add  sendTextGroup group topGroup 
        toolkit_set_property  sendTextGroup expandableX false
        toolkit_set_property  sendTextGroup expandableY false
        toolkit_set_property  sendTextGroup itemsPerRow 1
        toolkit_set_property  sendTextGroup title "Send Data"

        toolkit_add  sendTextText text sendTextGroup 
        toolkit_set_property  sendTextText expandableX false
        toolkit_set_property  sendTextText expandableY false
        toolkit_set_property  sendTextText preferredWidth 200
        toolkit_set_property  sendTextText preferredHeight 100
        toolkit_set_property  sendTextText editable true
        toolkit_set_property  sendTextText htmlCapable false
        toolkit_set_property  sendTextText text ""

        toolkit_add  sendTextButton button sendTextGroup 
        toolkit_set_property  sendTextButton enabled true
        toolkit_set_property  sendTextButton expandableX false
        toolkit_set_property  sendTextButton expandableY false
        toolkit_set_property  sendTextButton text "Send Now"
        toolkit_set_property  sendTextButton onClick {::Test::sendText}

        #
        # receiveText widgets
        #
        toolkit_add  receiveTextGroup group topGroup 
        toolkit_set_property  receiveTextGroup expandableX false
        toolkit_set_property  receiveTextGroup expandableY false
        toolkit_set_property  receiveTextGroup itemsPerRow 1
        toolkit_set_property  receiveTextGroup title "Receive Data"

        toolkit_add  receiveTextText text receiveTextGroup 
        toolkit_set_property  receiveTextText expandableX false
        toolkit_set_property  receiveTextText expandableY false
        toolkit_set_property  receiveTextText preferredWidth 200
        toolkit_set_property  receiveTextText preferredHeight 100
        toolkit_set_property  receiveTextText editable false
        toolkit_set_property  receiveTextText htmlCapable false
        toolkit_set_property  receiveTextText text ""

        return -code ok
    }
    
    proc updateDashboard {} {

        if { ${::Test::dashboardActive} > 0 } {

                toolkit_set_property  ledsGroup title "LED State"
                if { [ expr ${::Test::ledValue} & 0x01 &  \
                            ${::Test::Switch_off} ] } {
                    toolkit_set_property  led0LED color "green"
                    set ::Test::Switch_off  0
                } else {
                    toolkit_set_property  led0LED color "green_off"
                    set ::Test::Switch_off  1
                }
                if { [ expr ${::Test::ledValue} & 0x02 ] } {
                    toolkit_set_property  led1LED color "green"
                } else {
                    toolkit_set_property  led1LED color "green_off"
                }
        }
    }
}
::Test::dashBoard