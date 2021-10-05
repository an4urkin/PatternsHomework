from abc import ABC

import random


class BaseMediator(ABC):

    def notify(self, sender: object, event: str):
        pass
    
    def trigger(self, sender: object, event: str, argument):
        pass


class ConcreteMediator(BaseMediator):
    
    def __init__(self, unit1, unit2, unit3):
        self._unit1 = unit1
        self._unit1.mediator = self
        self._unit2 = unit2
        self._unit2.mediator = self
        self._unit3 = unit3
        self._unit3.mediator = self

        self._dict_events =	{
            "Bad Price": "self._unit3.raise_Error",
            "Factory Error": "self._unit3.raise_Error",
            "Place Order": "self._unit1.start",
            "Start Production": "self._unit2.produce",
            "Produce": "self._unit2.make",
            "Make Item": "self._unit2.pack",
            "Pack Item": "self._unit2.transfer",
            "Transfer Package": "self._unit2.ship",
            "Shipped": "self._unit3.ship_Order"
        }

    def notify(self, sender: object, event: str):
        print("\n[*] Mediator got "+ event +" and passes next:")
        call = self._dict_events[event]
        eval(call + "()")
        
    def trigger(self, sender: object, event: str, argument):
        print("\n[*] Mediator got "+ event +" and passes next:")
        call = self._dict_events[event]
        eval(call + "(argument)")


class BaseUnit:

    def __init__(self, mediator: BaseMediator = None):
        self._mediator = mediator

    def mediator(self):
        return self._mediator


class Factory(BaseUnit):
    
    def make(self, task):
        product = task + "."
        print("\nFactory sends: Make Item.")
        self.mediator.trigger(self, "Make Item", product)

    def pack(self, item):
        package = "package with " + item
        print("\nFactory sends: Pack Item.")
        self.mediator.trigger(self, "Pack Item", package)

    def produce(self, task):
        print("\nOrder proceeded to Factory.")
        print("Factory sends: Produce.")
        self.mediator.trigger(self, "Produce", task)

    def ship(self, order):
        print("\nFactory sends: Ship Order.")
        self.mediator.trigger(self, "Shipped", order)

    def transfer(self, package):
        order = "Transfered " + package
        print("\nFactory sends: Transfer Package.")
        self.mediator.trigger(self, "Transfer Package", order)


class Inspection(BaseUnit):

    def check_FactoryStatus(self, task):
        if len(task) != 0:
            return True

        return False

    def check_Price(self, price):
        if price < 1000:
            return True

        return False

    def create_Task(self):
        form_task = random.randint(0,2)

        if form_task == 0:
            task = ""

        elif form_task == 1:
            task = "Yogurt1"

        else:
            task = "Yogurt2"

        return task

    def start(self, price) -> None:
        print("\nOrder proceeded to Inspection.")

        if not self.check_Price(price):
            print("Inspection sends: Bad Price")
            self.mediator.notify(self, "Bad Price")

        else:
            task = self.create_Task()

            if self.check_FactoryStatus(task):
                print("Inspection sends: Start Production.")
                self.mediator.trigger(self, "Start Production", task)

            else:
                print("Inspection sends: Factory Error")
                self.mediator.notify(self, "Factory Error")
        

class DeliveryService(BaseUnit):

    def post_Order(self, price):
        print("\nOrder proceeded to Delivery Service.")
        print("Delivery Service sends: Place Order")
        self.mediator.trigger(self, "Place Order", price)

    def ship_Order(self, info):
        print("\nProduced item proceeded to Delivery Service.")
        print("Delivery Service sends: " + info)

    def raise_Error(self):
        print("\nDelivery Service sends: ERROR, order cannot be shipped.")


if __name__ == "__main__":

    insp = Inspection()
    fact = Factory()
    delv = DeliveryService()

    mediator = ConcreteMediator(insp, fact, delv)

    price = 100

    print("\nClient sends order to Delivery Service.")

    delv.post_Order(price)
