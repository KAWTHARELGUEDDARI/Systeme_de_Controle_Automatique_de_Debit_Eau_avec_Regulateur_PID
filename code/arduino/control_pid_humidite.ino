#include <LiquidCrystal.h>

// ========== PINS ==========
const int capteurHumiditePin = A0;
const int potentiometrePin = A1;
const int relaisPin = 7;

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// ========== VARIABLES PID ==========
float Kp = 3.0;
float Ki = 0.5;
float Kd = 1.0;

float setpoint = 50.0;
float humiditeActuelle = 0;
float erreur = 0;
float erreurPrecedente = 0;
float integrale = 0;
float derivee = 0;
float sortiePID = 0;

unsigned long dernierTemps = 0;
float dt = 0;

const float integraleMax = 100.0;
const float integraleMin = -100.0;

// ========== SETUP ==========
void setup() {
  pinMode(relaisPin, OUTPUT);
  digitalWrite(relaisPin, HIGH);

  lcd.begin(16, 2);
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Systeme PID");
  lcd.setCursor(0, 1);
  lcd.print("Demarrage...");
  delay(2000);

  lcd.clear();
  dernierTemps = millis();
}

// ========== LOOP ==========
void loop() {

  // ===== 1. LECTURE CAPTEUR =====
  int valeurCapteur = analogRead(capteurHumiditePin);
  humiditeActuelle = map(valeurCapteur, 1023, 0, 0, 100);
  humiditeActuelle = constrain(humiditeActuelle, 0, 100);

  // ===== 2. LECTURE POTENTIOMÈTRE =====
  int valeurPot = analogRead(potentiometrePin);
  setpoint = map(valeurPot, 0, 1023, 30, 80);

  // ===== 3. CALCUL TEMPS =====
  unsigned long maintenant = millis();
  dt = (maintenant - dernierTemps) / 1000.0;
  if (dt <= 0) dt = 0.1;
  dernierTemps = maintenant;

  // ===== 4. CALCUL PID =====
  erreur = setpoint - humiditeActuelle;

  float proportionnel = Kp * erreur;

  integrale += erreur * dt;
  integrale = constrain(integrale, integraleMin, integraleMax);
  float integral = Ki * integrale;

  derivee = (erreur - erreurPrecedente) / dt;
  float derivatif = Kd * derivee;

  sortiePID = proportionnel + integral + derivatif;
  erreurPrecedente = erreur;

  // ===== 5. COMMANDE RELAIS =====
  if (sortiePID > 0 && humiditeActuelle < setpoint - 3) {
    digitalWrite(relaisPin, LOW);
  } else {
    digitalWrite(relaisPin, HIGH);
  }

  // ===== 6. AFFICHAGE LCD (STABLE) =====

  // Ligne 1 : Humidité + Setpoint
  lcd.setCursor(0, 0);
  lcd.print("H:");
  lcd.print(humiditeActuelle, 1);
  lcd.print("% SP:");
  lcd.print((int)setpoint);
  lcd.print("%   ");

  // Ligne 2 : PID + état
  lcd.setCursor(0, 1);
  lcd.print("PID:");
  lcd.print(sortiePID, 1);

  if (digitalRead(relaisPin) == LOW) {
    lcd.print(" ON ");
  } else {
    lcd.print(" OFF");
  }
  lcd.print("   ");

  delay(300);
}
