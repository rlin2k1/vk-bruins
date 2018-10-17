#include "PS4BT.h"
#include "usbhub.h"
#include <Servo.h>


#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif
#include <SPI.h>

//setup for bluetooth dongle and the controller
USB Usb;
BTD Btd(&Usb);
PS4BT PS4(&Btd, PAIR);
Servo shoulder;
Servo elbow;
Servo cuff;
Servo wrist;
Servo gripper;

//define variables for the servos
const int BASE = 41;
const int SHOULDER = 42; 
const int ELBOW = 43;
const int CUFF = 44;
const int WRIST = 49;
const int GRIPPER = 46;
const int def_angle = 1500;
const int B_CAM = 1500;
const int S_CAM = 1600;
const int E_CAM = 1200;
const int C_CAM = 1500;
const int W_CAM = 600;
int b_angle = 1500;
int s_angle = 1500;
int e_angle = 1500;
int c_angle = 1500;
int w_angle = 1500;
int g_angle = 90;
bool Open = true;
bool usingWrist = false;

//digital outputs for motors 
const int IN1=22;
const int IN2=23;
const int ENA=2;

const int IN3=24;
const int IN4=25;
const int ENB=3;

const int IN5=26;
const int IN6=27;
const int ENC=4;

const int IN7=28;
const int IN8=29;
const int END=5;


//variables for camera

Servo cam_base;
Servo cam_tilt;

const int CAM_BASE = 37;
const int CAM_TILT = 38;

int cam_base_angle = 1500;
int cam_tilt_angle = 1500;

bool usingCamera = false;

bool show = true;


void setup() {
  Serial.begin(115200);
  
  //set the pinmode
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);
     
  pinMode(IN4, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(ENB, OUTPUT);
     
  pinMode(IN5, OUTPUT);
  pinMode(IN6, OUTPUT);
  pinMode(ENC, OUTPUT);

  pinMode(IN7, OUTPUT);
  pinMode(IN8, OUTPUT);
  pinMode(END, OUTPUT);
  
  //Setup for servos
  base.attach(BASE);
  base.writeMicroseconds(def_angle);
  shoulder.attach(SHOULDER);
  shoulder.writeMicroseconds(S_CAM);
  elbow.attach(ELBOW);
  elbow.writeMicroseconds(E_CAM);
  cuff.attach(CUFF);
  cuff.writeMicroseconds(C_CAM);
  wrist.attach(WRIST);
  wrist.writeMicroseconds(W_CAM);
  gripper.attach(GRIPPER);
  gripper.write(90);

  //setup for camera
  cam_base.attach(CAM_BASE);
  cam_base.writeMicroseconds(cam_base_angle);
  cam_tilt.attach(CAM_TILT);
  cam_tilt.writeMicroseconds(cam_tilt_angle);

  #if !defined(__MIPSEL__)
  while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
  #endif
  if (Usb.Init() == -1) {
    Serial.print(F("\r\nOSC did not start"));
    while (1); // Halt
  }
  Serial.print(F("\r\nPS4 Bluetooth Library Started"));
}
void loop() 
{
  Usb.Task();
  if(PS4.connected())
  {
    if(PS4.getButtonClick(OPTIONS))
    {
      state = 1;
    }
    else if(PS4.getButtonClick(SELECT))
    {
      state = 2;
    }
    else if(PS4.getButtonClick(TOUCHPAD))
    {
      state =3;
    }


    switch(state)
    {
      case 1:
      default:
      {
        Serial.println("Switch to MOTOR CONTROL");
        motorControl();
        break;
      }
      case 2:
      {
        Serial.println("Switch to ARM CONTROL");
        armControl();
        break;
      }
      case 3:
      {
        Serial.println("Switch to CAMERA CONTROL");
        cameraControl();
        break;
      }
    }

 /*   if(PS4.getButtonClick(PS)) 
    {
      Serial.print(F("DISCONNECTED"));
      PS4.disconnect();
    }*/

    
  }


}



//arm control function
void armControl()
{
  if(PS4.getButtonClick(R1))
  {
    if(usingWrist)
    {
      usingWrist = false;
    }
    else
    {
      usingWrist = true;
    }
   }
    
//BASE AND SHOULDER MOVEMENTS
    x = PS4.getAnalogHat(LeftHatX);
    y = PS4.getAnalogHat(LeftHatY);
    if(!usingWrist)
    {
      //Base
      if(x < 100)
      {
         if(((y < 100 || y > 154) && x < 50) || (y > 100 && y < 154))
        {
          
          if(b_angle != 600)
          {
            b_angle-=5;
            base.writeMicroseconds(b_angle);
            Serial.print("b_angle: ");
            Serial.println(b_angle);
            delay(5);
          }
        }
      }

      if(x > 154)
      {
        if(((y < 100 || y > 154) && x > 225) || (y > 100 && y < 154))
        {
          if(b_angle != 2400)
          {
            b_angle+=5;
            base.writeMicroseconds(b_angle);
            Serial.print("b_angle: ");
            Serial.println(b_angle);
            delay(5);
          }
        }
      }

      //Shoulder
      if(y < 100)
      {
        if(((x < 100 || x > 154) && y < 50) || (x > 100 && x < 154))
        {
          if(s_angle != 600)
          {
            s_angle-=5;
            shoulder.writeMicroseconds(s_angle);
            Serial.print("s_angle: ");
            Serial.println(s_angle);
            delay(5);
          }
        }
      }
      if(y > 154)
      {
        if(((x < 100 || x > 154) && y > 225) || (x > 100 && x < 154))
        {
          if(s_angle != 2400)
          {
            s_angle+=5;
            shoulder.writeMicroseconds(s_angle);
            Serial.print("s_angle: ");
            Serial.println(s_angle);
            delay(5);
          }
        }
      }
    }

//ELBOW AND CUFF MOVEMENTS USING ANALOG STICK
    x = PS4.getAnalogHat(RightHatX);
    y = PS4.getAnalogHat(RightHatY);
    //Elbow 
    if(y < 100)
    {
      if(((x < 100 || x > 154) && y < 50) || (x > 100 && x < 154))
      {
        if(e_angle != 2400)
        {
          e_angle+=5;
          elbow.writeMicroseconds(e_angle);
          Serial.print("e_angle: ");
          Serial.println(e_angle);
          delay(5);
        }
      }
    }

    if(y > 154)
    {
      if(((x < 100 || x > 154) && y > 225) || (x > 100 && x < 154))
      {
        if(e_angle != 600)
        {
          e_angle-=5;
          elbow.writeMicroseconds(e_angle);
          Serial.print("e_angle: ");
          Serial.println(e_angle);
          delay(5);
        }
      }
    }


    //Cuff
    if(x < 100)
    {
      if(((y < 100 || y > 154) && x < 50) || (y > 100 && y < 154))
      {
        if(c_angle != 600)
        {
          c_angle-=5;
          cuff.writeMicroseconds(c_angle);
          Serial.print("c_angle: ");
          Serial.println(c_angle);
          delay(5);
        }
      }
    }

    if(x > 154)
    {
      if(((y < 100 || y > 154) && x > 225) || (y > 100 && y < 154))
      {
        if(c_angle != 2400)
         {
          c_angle+=5;
          cuff.writeMicroseconds(c_angle);
          Serial.print("c_angle: ");
          Serial.println(c_angle);
          delay(5);
         }
      }
    }
//R1 to switch to wrist control
    if(usingWrist)
    {
      y = PS4.getAnalogHat(LeftHatY);
      if(y < 100)
      {
        if(w_angle != 2300)
          {
             w_angle+=5;
             wrist.writeMicroseconds(w_angle);
             delay(5);
          }
      }
      if(y > 154)
      {
        if(w_angle != 600)
          {
            w_angle-=5;
            wrist.writeMicroseconds(w_angle);
            delay(5);
          }
      }
    }
    
//GRIPPER OPEN/CLOSE USING TRIANGLE
    if(PS4.getButtonClick(TRIANGLE))
    {
      if(Open)
      {
        gripper.write(42);
        Open = false;
      }
      else
      {
        gripper.write(90);
        Open = true;
      }
    }
//reset arm positions
    if(PS4.getButtonClick(CROSS))
    {
      b_angle = 1500;
      s_angle = 1500;
      e_angle = 1500;
      c_angle = 1500;
      w_angle = 1500;
      g_angle = 90;
      base.writeMicroseconds(b_angle);
      shoulder.writeMicroseconds(s_angle);
      elbow.writeMicroseconds(e_angle);
      cuff.writeMicroseconds(c_angle);
      wrist.writeMicroseconds(w_angle);
      gripper.write(g_angle);
    }
}

void motorControl()
{
  int analogL2 = PS4.getAnalogButton(L2);
  int analogR2 = PS4.getAnalogButton(R2);
  bool Click = PS4.getButtonClick(TRIANGLE);
  
  if(PS4.getAnalogHat(LeftHatX) > 154 || PS4.getAnalogHat(LeftHatX) < 100)
  {
    //go left
    if(PS4.getAnalogHat(LeftHatX) < 100)
    {
      Motor1_Backward(analogR2);
      Motor4_Forward(analogR2);
      //Motor2_Forward(analogR2);
      //Motor3_Backward(analogR2);
      Serial.println("Left");
    }
    //go right
    else
    {
      Motor1_Forward(analogR2);
      Motor4_Backward(analogR2);
      Serial.println("Right");
    }
  }
  
  //goes forward if R2 is detected
  else if (PS4.getAnalogButton(R2) > 0)
  {
    Motor1_Forward(analogR2);
   // Motor2_Forward(analogR2);
    //Motor3_Forward(analogR2);
    Motor4_Forward(analogR2);
    Serial.println("forward");
  }  
  //go backward if L2 is detected 
  else if (PS4.getAnalogButton(L2) > 0)
  {
    Motor1_Backward(analogL2);
    //Motor2_Backward(analogL2);
    //Motor3_Backward(analogL2);
    Motor4_Backward(analogL2);
    Serial.println("Backward");
  }
  //does nothing
  else
  {
    Motor1_Brake();
    //Motor2_Brake();
    //Motor3_Brake();
    Motor4_Brake();
  }

  if(Click)
  {
    base.writeMicroseconds(B_CAM);
    shoulder.writeMicroseconds(S_CAM);
    elbow.writeMicroseconds(E_CAM);
    cuff.writeMicroseconds(C_CAM);
    wrist.writeMicroseconds(W_CAM);
    gripper.write(90);
  }
  /*
}
  int analogL2 = PS4.getAnalogButton(L2);
  int analogR2 = PS4.getAnalogButton(R2);
  int x = PS4.getAnalogHat(LeftHatX);
  bool Click = PS4.getButtonClick(TRIANGLE);
  const int Speed = 255;
  
  if(analogR2>100)
  {
    if(x < 100)
    {
      Motor1_Forward(Speed);
      Motor3_Backward(Speed);
      Motor2_Brake();
      Motor4_Brake();
    }
    else if(x > 154)
    {
      Motor2_Forward(Speed);
      Motor4_Backward(Speed);
      Motor1_Brake();
      Motor3_Brake();
    }
    else
    {
      Motor1_Forward(Speed);
      Motor2_Forward(Speed);
      Motor3_Forward(Speed);
      Motor4_Forward(Speed);
    }
    Serial.print("R2: ");
    Serial.println(analogR2);
  }
  else if(analogL2>0)
  {
    if(x < 100)
    {
      Motor1_Brake();
      Motor3_Brake();
      Motor2_Forward(Speed);
      Motor4_Backward(Speed);
    }
    else if( x > 154)
    {
      Motor2_Brake();
      Motor4_Brake();
      Motor1_Forward(Speed);
      Motor3_Backward(Speed);
    }
    else
    {
      Motor1_Backward(Speed);
      Motor2_Backward(Speed);
      Motor3_Backward(Speed);
      Motor4_Backward(Speed);
    }
    Serial.print("L2: ");
    Serial.println(analogL2);
  }
  if(Click)
  {
    base.writeMicroseconds(B_CAM);
    shoulder.writeMicroseconds(S_CAM);
    elbow.writeMicroseconds(E_CAM);
    cuff.writeMicroseconds(C_CAM);
    wrist.writeMicroseconds(W_CAM);
    gripper.write(90);
  }*/
}


//*********************************************************
//*********************************************************
//*****************MOTOR CONTROLS**************************
//*********************************************************
//*********************************************************
    
void Motor1_Forward(int Speed) 
{
     digitalWrite(IN3,HIGH); 
     digitalWrite(IN4,LOW);  
     analogWrite(ENB,Speed);
}
  
void Motor1_Backward(int Speed) 
{    
     digitalWrite(IN3,LOW); 
     digitalWrite(IN4,HIGH);  
     analogWrite(ENB,Speed);
}
void Motor1_Brake()
{
     digitalWrite(IN3,LOW); 
     digitalWrite(IN4,LOW); 
}



void Motor2_Backward(int Speed) 
{
     digitalWrite(IN5,HIGH); 
     digitalWrite(IN6,LOW);  
     analogWrite(ENC,Speed);
}
  
void Motor2_Forward(int Speed) 
{    
     digitalWrite(IN5,LOW); 
     digitalWrite(IN6,HIGH);  
     analogWrite(ENC,Speed);
}
void Motor2_Brake()      
{
     digitalWrite(IN5,LOW); 
     digitalWrite(IN6,LOW); 
}     
void Motor3_Forward(int Speed) 
{
     digitalWrite(IN7,HIGH); 
     digitalWrite(IN8,LOW);  
     analogWrite(END,Speed);
}
  
void Motor3_Backward(int Speed) 
{    
     digitalWrite(IN7,LOW); 
     digitalWrite(IN8,HIGH);  
     analogWrite(END,Speed);
}
void Motor3_Brake()
{
     digitalWrite(IN7,LOW); 
     digitalWrite(IN8,LOW); 
}

void Motor4_Backward(int Speed) 
{
     digitalWrite(IN1,HIGH); 
     digitalWrite(IN2,LOW);  
     analogWrite(ENA,Speed);
}
  
void Motor4_Forward(int Speed) 
{    
     digitalWrite(IN1,LOW); 
     digitalWrite(IN2,HIGH);  
     analogWrite(ENA,Speed);
}
void Motor4_Brake()      
{
     digitalWrite(IN1,LOW); 
     digitalWrite(IN2,LOW); 
} 

void cameraControl()
{
  x = PS4.getAnalogHat(LeftHatX);
  y = PS4.getAnalogHat(LeftHatY);
  
  if(x < 100)
  {
    
    if(((y < 100 || y > 154) && x < 50) || (y > 100 && y < 154))
    {
      if(cam_base_angle != 600)
      {
        cam_base_angle-=5;
        cam_base.writeMicroseconds(cam_base_angle);
        Serial.print("cam_base_angle: ");
        Serial.println(cam_base_angle);
        delay(5);
      }
    }
  }

  if(x > 154)
  {
    if(((y < 100 || y > 154) && x > 225) || (y > 100 && y < 154))
    {
      if(cam_base_angle != 2400)
      {
        cam_base_angle+=5;
        cam_base.writeMicroseconds(cam_base_angle);
        Serial.print("cam_base_angle: ");
        Serial.println(cam_base_angle);
        delay(5);
      }
    }
  }


  if(y < 100)
  {
    if(((x < 100 || x > 154) && y < 50) || (x > 100 && x < 154))
    {
      if(cam_tilt_angle != 600)
      {
        cam_tilt_angle-=5;
        cam_tilt.writeMicroseconds(cam_tilt_angle);
        Serial.print("cam_tilt_angle: ");
        Serial.println(cam_tilt_angle);
        delay(5);
       }
     }
  }
  if(y > 154)
  {
    if(((x < 100 || x > 154) && y > 225) || (x > 100 && x < 154))
    {
      if(cam_tilt_angle != 2400)
      {
        cam_tilt_angle+=5;
        cam_tilt.writeMicroseconds(cam_tilt_angle);
        Serial.print("cam_tilt_angle: ");
        Serial.println(cam_tilt_angle);
        delay(5);
      }
    }
  } 
}

