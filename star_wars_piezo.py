# Circuit Playground Express Star Wars
#
# a simple fun way to test the play_tone function
#
# MIT License (https://opensource.org/licenses/MIT)

from adafruit_circuitplayground.express import cpx
import time

note_c = 261
note_d = 294
note_e = 329
note_f = 349
note_g = 391
note_gS = 415
note_a = 440
note_aS = 455
note_b = 466
note_cH = 523
note_cSH = 554
note_dH = 587
note_dSH = 622
note_eH = 659
note_fH = 698
note_fSH = 740
note_gH = 784
note_gSH = 830
note_aH = 880

def second_section():
    # second section start
    cpx.play_tone(note_aH, .500)
    cpx.play_tone(note_a, .300)
    cpx.play_tone(note_a, .150)
    cpx.play_tone(note_aH, .500)
    cpx.play_tone(note_gSH, .325)
    cpx.play_tone(note_gH, .175)
    cpx.play_tone(note_fSH, .125)
    cpx.play_tone(note_fH, .125)    
    cpx.play_tone(note_fSH, .250)

    time.sleep(.325)

    cpx.play_tone(note_aS, .250)
    cpx.play_tone(note_dSH, .500)
    cpx.play_tone(note_dH, .325)  
    cpx.play_tone(note_cSH, .175)  
    cpx.play_tone(note_cH, .125)  
    cpx.play_tone(note_b, .125)  
    cpx.play_tone(note_cH, .250)  

    time.sleep(.350)
    #second end

def play():
    cpx.play_tone(note_a, .500)
    cpx.play_tone(note_a, .500)    
    cpx.play_tone(note_a, .500)
    cpx.play_tone(note_f, .350)
    cpx.play_tone(note_cH, .150)  
    cpx.play_tone(note_a, .500)
    cpx.play_tone(note_f, .350)
    cpx.play_tone(note_cH, .150)
    cpx.play_tone(note_a, .650)

    time.sleep(.500)

    cpx.play_tone(note_eH, .500)
    cpx.play_tone(note_eH, .500)
    cpx.play_tone(note_eH, .500)  
    cpx.play_tone(note_fH, .350)
    cpx.play_tone(note_cH, .150)
    cpx.play_tone(note_gS, .500)
    cpx.play_tone(note_f, .350)
    cpx.play_tone(note_cH, .150)
    cpx.play_tone(note_a, .650)

    time.sleep(.500)

    second_section()

    # //Variant 1
    cpx.play_tone(note_f, .250)  
    cpx.play_tone(note_gS, .500)  
    cpx.play_tone(note_f, .350)  
    cpx.play_tone(note_a, .125)
    cpx.play_tone(note_cH, .500)
    cpx.play_tone(note_a, .375)  
    cpx.play_tone(note_cH, .125)
    cpx.play_tone(note_eH, .650)

    time.sleep(.500)

    # //Repeat second section
    # //secondSection()
    second_section()

    # //Variant 2
    cpx.play_tone(note_f, .250)  
    cpx.play_tone(note_gS, .500)  
    cpx.play_tone(note_f, .375)  
    cpx.play_tone(note_cH, .125)
    cpx.play_tone(note_a, .500)  
    cpx.play_tone(note_f, .375)  
    cpx.play_tone(note_cH, .125)
    cpx.play_tone(note_a, .650)  

    time.sleep(.650)

play()
