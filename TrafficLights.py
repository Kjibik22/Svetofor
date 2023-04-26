from enum import Enum
from flask import jsonify
from time import sleep


class TrafficColor(Enum):
    Red = 1
    Yellow = 2
    Green = 3
    BlinkGreen = 4
    SecondYellow = 5
    Disable = 6
    Broken = 7
    Repairing = 8

    def Next(self):
        v = self.value + 1
        if v > TrafficColor.SecondYellow.value: v = TrafficColor.Red.value
        return TrafficColor(v)

    def Prev(self):
        v = self.value - 1
        if v < TrafficColor.Red.value: v = TrafficColor.SecondYellow.value
        return TrafficColor(v)


class TrafficLights:
    def __init__(self):
        self.TimeArray = [10] * TrafficColor.SecondYellow.value
        self.CarState = TrafficColor.Green
        self.PeopleState = TrafficColor.Red
        self.ResponsePeopleCD = 0
        self.TrafficOn = True
        self.setTime()

    def GetPeopleState(self, state):
        if state == TrafficColor.Broken:
            return TrafficColor.Broken
        if state == TrafficColor.Red:
            if self.timer < self.getTime() / 3:
                return TrafficColor.BlinkGreen
            else:
                return TrafficColor.Green
        else:
            return TrafficColor.Red

    def setTime(self):
        self.timer = self.TimeArray[self.CarState.value - 1]

    def getTime(self):
        return self.TimeArray[self.CarState.value - 1]

    def UpdateTimer(self, time):
        if self.TrafficOn == True:
            self.TimeArray[self.CarState.value - 1] = int(time)
            self.setTime()

    def TrafficStart(self):
        while True:
            sleep(1)
            if self.CarState == TrafficColor.Broken:
                continue
            if self.TrafficOn == True:

                if self.ResponsePeopleCD > 0 and self.CarState == TrafficColor.Green: self.ResponsePeopleCD = self.ResponsePeopleCD - 1

                self.timer = self.timer - 1
                if self.timer <= 0:
                    self.CarState = self.CarState.Next()
                    self.setTime()
                self.PeopleState = self.GetPeopleState(self.CarState)

    def PeopleButtonPressed(self):
        if self.ResponsePeopleCD <= 0 and self.CarState == TrafficColor.Green and self.timer > int(self.getTime() / 4):
            self.ResponsePeopleCD = self.TimeArray[TrafficColor.Green.value - 1] / 2
            self.timer = int(self.getTime() / 4)
            return jsonify(ButtonResponse='Светофор сменит сигнал через ' + str(int(self.timer)) + ' секунд')
        elif self.ResponsePeopleCD > 0:
            return jsonify(ButtonResponse='Кнопка будет доступна через ' + str(
                int(self.ResponsePeopleCD)) + ' секунд движения автомобилей')
        else:
            return jsonify(ButtonResponse='Подождите пожалуйста')

    def DisableTrafficLight(self):
        self.TrafficOn = False

    def EnableTrafficLight(self):
        self.TrafficOn = True

    def PrevState(self):
        self.CarState = self.CarState.Prev()
        self.setTime()
        self.PeopleState = self.GetPeopleState(self.CarState)

    def NextState(self):
        self.CarState = self.CarState.Next()
        self.setTime()
        self.PeopleState = self.GetPeopleState(self.CarState)

    def BrakeTrafficLight(self):
        self.CarState = TrafficColor.Broken
        self.PeopleState = self.GetPeopleState(self.CarState)

    def ResponseState(self):
        if self.TrafficOn == True:
            return jsonify(
                CarState=self.CarState.name,
                PeopleState=self.PeopleState.name,
                Timer=int(self.timer),
                MaxTimer=self.getTime())
        else:
            return jsonify(
                CarState=TrafficColor.Disable.name,
                PeopleState=TrafficColor.Disable.name,
                Timer=int(self.timer),
                MaxTimer=self.getTime())

