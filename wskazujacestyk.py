import cv2
import mediapipe as mp
import time
import os
import pdb
import sys


#inicjalizacja detektora dloni
hands = mp.solutions.hands.Hands(static_image_mode=True)
mp_drawing = mp.solutions.drawing_utils
counter = 0
hej = "memoryinject"


# na potrzeby prymitwynego debuguu oraz manipulacji pamiecia procesu
# input("wpisz:")

#handler kamery podlaczonej do urzadzenia
image = cv2.VideoCapture(0)

while True:
    ret, frame = image.read()
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # debug za pomoca pdb
    # breakpoint()

        #detekcja dloni i landmarkow
    results = hands.process(image_rgb)
    if results.multi_hand_landmarks:
        first_hand = results.multi_hand_landmarks[0]
        wskazujacy_firstrenka = first_hand.landmark[8]
        #print("pierwsza:" + str(wskazujacy_firstrenka.x))
    try:
        second_hand = results.multi_hand_landmarks[1]
        wskazujacy_secrenka = second_hand.landmark[8]
        #print(wskazujacy_secrenka.x)
    except Exception:
        pass

    #time.sleep(1)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            #rysuj landmarki na obrazku
            mp_drawing.draw_landmarks(image_rgb, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
    if 'wskazujacy_firstrenka' in locals() and 'wskazujacy_secrenka' in locals():
        if wskazujacy_firstrenka.x > wskazujacy_secrenka.x:
            #kalkulacja roznicy w polozeniu palcy wskazujacych na osi X obu dloni
            calculation = wskazujacy_firstrenka.x - wskazujacy_secrenka.x
            #jezeli wynik tej kalkulacji jest ponizej 0.025 mozna z duzym prawdopodobienstwem stwierdzic ze palce wskazujace sie dotykaja
            if calculation < 0.025:
                print("Wskazujace sie dotyakjo!" + str(counter) + hej)
                counter = counter + 1
                #prawie zapomnialem usunac credentiale :D
                os.system('"C:\\Program Files (x86)\\WinSCP\\WinSCP.exe" scp://root:eeeee@192.168.9.69/')
            del wskazujacy_firstrenka
            del wskazujacy_secrenka 
        else:
            #kalkulacja roznicy w polozeniu palcy wskazujacych na osi X obu dloni
            calculation = wskazujacy_secrenka.x - wskazujacy_firstrenka.x
            #jezeli wynik tej kalkulacji jest ponizej 0.025 mozna z duzym prawdopodobienstwem stwierdzic ze palce wskazujace sie dotykaja
            if calculation < 0.025:
                
                print("Wskazujace sie dotyakjo!" + str(counter) + hej)
                counter = counter + 1
                #wyzwalana akcja podczas styku wskazujacych (polaczenie SCP do jakiegos serwera)
                os.system('"C:\\Program Files (x86)\\WinSCP\\WinSCP.exe" scp://root:password@192.168.0.1/')
            #
            #usuwamy zmienne na ktorych bazuje wczesniejszy if (jezeli wykryje dwie dlonie)  i robimy powrot do poczatku petli while
            del wskazujacy_firstrenka
            del wskazujacy_secrenka
            
    #handler okna gui z przetworzonym obrazem kamery
    cv2.imshow("Wynik", image_rgb)
    cv2.waitKey(1)
