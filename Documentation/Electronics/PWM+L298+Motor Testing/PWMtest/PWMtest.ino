void setup() {
  // put your setup code here, to run once:
  pinMode(11, OUTPUT);
  pinMode(A5, INPUT);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  Serial.begin(9600);
}

int inputA0;
int inputA1;
int spd;

void loop() {
  // put your main code here, to run repeatedly:
  spd = analogRead(A5);
  analogWrite(11, map(spd, 0, 1023, 0, 255));
  inputA0 = analogRead(A0);
  inputA1 = analogRead(A1);

  Serial.print(spd);
  Serial.print("\t");
  Serial.print(map(spd,0,1023,0,255));

  Serial.print("\t A0 \t");
  Serial.print(inputA0);

  
  Serial.print("\t A1 \t");
  Serial.println(inputA1);
}
