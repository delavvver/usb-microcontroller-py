# Управление микроконтроллером по USB

---

<details>
<summary><b>Задание</b></summary>

Для передачи команд управления на микроконтроллер предлагается использовать структурированные пакеты данных. Такой подход упрощает обработку входящей информации, повышает надёжность передачи и позволяет в дальнейшем расширять систему.

Предусмотрено два формата пакетов, предназначенных для разных типов данных.

### 1. Пакет команд управления

Данный формат предназначен для передачи команд управления микроконтроллером.

**Структура пакета:**

| Поле | Размер |
|---|---:|
| Заголовок | 1 байт |
| Команда | 1 байт |
| Полезная нагрузка | 5 байт |
| Окончание | 1 байт |
| **Итого** | **8 байт** |

**Особенности:**
- Фиксированная длина пакета — 8 байт.
- Поле команды определяет выполняемое действие.
- Полезная нагрузка содержит дополнительные параметры команды.
- Заголовок и окончание позволяют определить границы пакета.

При необходимости заголовок может содержать идентификатор команды или дополнительный признак, позволяющий обнаруживать ошибки передачи и некорректные пакеты.

### 2. Пакет передачи данных

Данный формат предназначен для передачи больших объёмов информации и данных переменной длины.

**Структура пакета:**

| Поле | Размер |
|---|---:|
| Заголовок | 1 байт |
| Длина | 1 байт |
| Данные | 1–254 байта |
| Проверочный блок | 1 байт |
| **Итого** | **4–257 байт** |

**Особенности:**
- Переменная длина пакета.
- Поле длины определяет количество передаваемых байт.
- Данные могут содержать произвольную полезную информацию.
- Проверочный блок предназначен для обнаружения ошибок при передаче.

<img width="575" height="346" alt="Структура пакета" src="https://github.com/user-attachments/assets/4e048c1f-1f3b-4e3b-975b-d5c5385db57b" />

</details>

---

<details>
<summary><b>Вывод</b></summary>

**Видеоматериалы:**

- https://youtu.be/7lEz1tKx6Oc
- https://youtu.be/fXgPZ03UauQ

**Результаты выполнения:**

<img width="994" alt="Результат 1" src="https://github.com/user-attachments/assets/657c4acf-806a-4014-be74-1f2e573a48e8" />

<img width="1002" alt="Результат 2" src="https://github.com/user-attachments/assets/76e3501a-8e26-4089-87ee-1136df539ba2" />

</details>

---

## Прошивка микроконтроллера

<details>
<summary><b>Исходный код</b></summary>

```cpp
#define HEADER 0xAA
#define END_BYTE 0x55

#define CMD_LED_ON 0x01
#define CMD_LED_OFF 0x02
#define CMD_LED_BLINK 0x03

#define CMD_SET_PIN 0x10
#define CMD_SET_MODE 0x20

#define MODE_OFF 0x00
#define MODE_ON 0x01
#define MODE_PWM 0x02
#define MODE_BLINK 0x03

const byte allowedPins[] = {4, 5, 12, 13, 14};
const byte PIN_COUNT = 5;

byte activePin = 4;

byte currentMode = MODE_OFF;
byte brightness = 0;
byte blinkFrequency = 1;

bool ledState = false;
unsigned long previousMillis = 0;


void setup() {
    Serial.begin(9600);

    analogWriteRange(255);
    analogWriteFreq(1000);

    pinMode(activePin, OUTPUT);
    digitalWrite(activePin, LOW);

    Serial.println("ESP8266 READY");
}


void loop() {

    if (Serial.available() >= 8) {

        byte packet[8];

        Serial.readBytes(packet, 8);

        if (packet[0] == HEADER &&
            packet[7] == END_BYTE) {

            byte command = packet[1];

            byte data[5];

            for (byte i = 0; i < 5; i++) {
                data[i] = packet[i + 2];
            }

            processCommand(command, data);
        }
    }

    updateBlink();
}

bool isAllowedPin(byte pin) {

    for (byte i = 0; i < PIN_COUNT; i++) {

        if (allowedPins[i] == pin) {
            return true;
        }
    }

    return false;
}


void setActivePin(byte newPin) {

    if (!isAllowedPin(newPin)) {
        Serial.println("ERROR: INVALID GPIO");
        return;
    }

    analogWrite(activePin, 0);
    digitalWrite(activePin, LOW);

    activePin = newPin;

    pinMode(activePin, OUTPUT);

    ledState = false;
    currentMode = MODE_OFF;

    digitalWrite(activePin, LOW);

    Serial.print("ACTIVE GPIO: ");
    Serial.println(activePin);
}

void setMode(byte mode, byte parameter) {

    if (mode > MODE_BLINK) {
        Serial.println("ERROR: INVALID MODE");
        return;
    }

    currentMode = mode;
    previousMillis = millis();

    switch (mode) {

        case MODE_OFF:

            brightness = 0;
            ledState = false;

            digitalWrite(activePin, LOW);

            Serial.println("MODE: OFF");
            break;


        case MODE_ON:

            brightness = 255;
            ledState = true;

            digitalWrite(activePin, HIGH);

            Serial.println("MODE: ON");
            break;


        case MODE_PWM:

            brightness = parameter;
            ledState = brightness > 0;

            analogWrite(activePin, brightness);

            Serial.print("MODE: PWM | BRIGHTNESS: ");
            Serial.println(brightness);
            break;


        case MODE_BLINK:

            if (parameter < 1 || parameter > 20) {
                currentMode = MODE_OFF;
                digitalWrite(activePin, LOW);

                Serial.println("ERROR: FREQUENCY MUST BE 1-20 HZ");
                return;
            }

            blinkFrequency = parameter;

            ledState = true;
            digitalWrite(activePin, HIGH);

            Serial.print("MODE: BLINK | FREQUENCY: ");
            Serial.println(blinkFrequency);
            break;
    }
}


void processCommand(byte command, byte data[]) {

    switch (command) {

        case CMD_SET_PIN:

            setActivePin(data[0]);
            break;


        case CMD_SET_MODE:

            setMode(data[0], data[1]);
            break;


        // Старые команды для совместимости
        case CMD_LED_ON:

            setMode(MODE_ON, 0);
            break;


        case CMD_LED_OFF:

            setMode(MODE_OFF, 0);
            break;


        case CMD_LED_BLINK:

            setMode(MODE_BLINK, data[4]);
            break;


        default:

            Serial.println("ERROR: UNKNOWN COMMAND");
            break;
    }
}

void updateBlink() {

    if (currentMode != MODE_BLINK) {
        return;
    }

    unsigned long currentMillis = millis();

    unsigned long interval = 500 / blinkFrequency;

    if (currentMillis - previousMillis >= interval) {

        previousMillis = currentMillis;

        ledState = !ledState;

        digitalWrite(
            activePin,
            ledState ? HIGH : LOW
        );
    }
}
```

</details>
