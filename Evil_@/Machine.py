from machine import PWM

camara = PWM(5 , PWM.Out())
Speaker = PWM(16 , PWM.Out())
mic = PWM(18 , PWM.In())
