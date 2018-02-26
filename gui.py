"""
This code demonstrates "bare bones" drag and drop
"""

try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
try:
    import Tkdnd
except ImportError:
    import tkinter.dnd as Tkdnd

class Dragged:
    """
    This is a thing to be dragged and dropped.
    """
    def __init__(self, button):
        self.button = button
        print("An instance of Dragged has been created for button %s" % (button))
        
    def dnd_end(self,Target,Event):
        #this gets called when we are dropped
        print("I have been dropped; Target=%s" % ('Target'))

class CanvasDnd(Canvas):
    """
    This is a canvas to which we have added a "dnd_accept" method, so it
    can act as a Target Widget for drag and drop. To prove that the Target
    Object can be different from the Target Widget, CanvasDnd accepts as
    argument "GiveDropTo" the object to which the dropped object is to 
    be given.
    """    
    def __init__(self, Master, GiveDropTo, **kw):
        Canvas.__init__(self, Master, kw)
        #Simply remember the TargetObject for later use.
        self.GiveDropTo = GiveDropTo

    def dnd_accept(self,Source,Event):
        #Tkdnd is asking us if we want to tell it about a TargetObject.
        #We do, so we pass it a reference to the TargetObject which was
        #given to us when we started
        print("Canvas: dnd_accept")
        return self.GiveDropTo

class FrameDnd(Frame):
    def __init__(self, Master, GiveDropTo, **kw):
        Frame.__init__(self,Master, kw)
        self.GiveDropTo = GiveDropTo

    def dnd_accept(self,Source,Event):
        print("Frame: dnd_accept")
        return self.GiveDropTo

class Receptor:
    """
    This is a thing to act as a TargetObject
    """
    def dnd_enter(self,Source,Event):
        #This is called when the mouse pointer goes from outside the
        #Target Widget to inside the Target Widget.
        # print ("Receptor: dnd_enter")
        pass
        
    def dnd_leave(self,Source,Event):
        #This is called when the mouse pointer goes from inside the
        #Target Widget to outside the Target Widget.
        # print ("Receptor: dnd_leave")
        pass
        
    def dnd_motion(self,Source,Event):
        #This is called when the mouse pointer moves withing the TargetWidget.
        # print ("Receptor: dnd_motion")
        pass
        
    def dnd_commit(self,Source,Event):
        #This is called if the DraggedObject is being dropped on us
        print ("Receptor: dnd_commit; Object received = %s" % str(Source))
        print("Accepting Frame Number = %s" % str(get_frame_num(Event.x)))
        # print(dir(Source))
        # print(Source.__class__)
        if isinstance(Source, Dragged):
            print("Received object is an instance of Dragged.class from button %s" % (Event.widget.cget('text')))
            if(get_frame_num(Event.x) in frame_dict):
                create_instruction_frame(get_frame_num(Event.x), Event.widget.cget('text'))
            else:
                print("Error, Invalid drop at x_coor: %s" % (str(Event.x)))
        else:
            print("Error: Received object was not an instance of Dragged.class.")

def create_instruction_frame(frame_num, button_name):
    frame = frame_dict.get(frame_num)
    l = Label(frame, text=button_name+" Command", fg='blue', wraplength=75).pack()  
    b = Button(frame, text='Remove').pack()
    b2 = Button(frame, text='Edit').pack()

def get_frame_num(x_coor):
    if(x_coor > 80 and x_coor <= 155):
        return 1
    elif(x_coor > 165 and x_coor <= 240):
        return 2
    elif(x_coor > 250 and x_coor <= 325):
        return 3
    elif(x_coor > 335 and x_coor <= 410):
        return 4
    elif(x_coor > 420 and x_coor <= 495):
        return 5
    elif(x_coor > 505 and x_coor <= 580):
        return 6
    elif(x_coor > 590 and x_coor <= 665):
        return 7
    elif(x_coor > 675 and x_coor <= 750):
        return 8
    else:
        return -1

def on_dnd_start(Event, button):
    """
    This is invoked by InitiationObject to start the drag and drop process
    """
    #Create an object to be dragged
    ThingToDrag = Dragged(button)
    
    #Pass the object to be dragged and the event to Tkdnd
    Tkdnd.dnd_start(ThingToDrag,Event)

Root = Tk()
Root.title('Robot Touch Controls')
Root.geometry('800x600')
#Create an object whose job is to act as a TargetObject, that is, to
# received the dropped object.
TargetObject = Receptor()

#Create a button to act as the InitiationObject and bind it to <ButtonPress> so
# we start drag and drop when the user clicks on it.
frame = Frame(Root)
frame.pack(side = LEFT)
Label(frame, text="Commands", fg='blue').pack()

Motors = Button(frame,text='Motors')
Motors.pack(side=BOTTOM)
Motors.bind('<ButtonPress>', lambda event: on_dnd_start(event, 'Motors'))
HeadTilt = Button(frame,text='HeadTilt')
HeadTilt.pack(side=BOTTOM)
HeadTilt.bind('<ButtonPress>', lambda event: on_dnd_start(event, 'HeadTilt'))
HeadTurn = Button(frame,text='HeadTurn')
HeadTurn.pack(side=BOTTOM)
HeadTurn.bind('<ButtonPress>',lambda event: on_dnd_start(event, 'HeadTurn'))
BodyTurn = Button(frame,text='BodyTurn')
BodyTurn.pack(side=BOTTOM)
BodyTurn.bind('<ButtonPress>',lambda event: on_dnd_start(event, 'BodyTurn'))
Pause = Button(frame,text='Pause')
Pause.pack(side=BOTTOM)
Pause.bind('<ButtonPress>',lambda event: on_dnd_start(event, 'Pause'))

#Create a canvas to act as the Target Widget for the drag and drop. Note that
# since we are going out of our way to have the Target Widget and the Target
# Object be different things, we pass a reference to the Target Object to
# the canvas we are creating.
frame1 = FrameDnd(Root, width=75, height = 400, GiveDropTo=TargetObject,relief=RAISED, borderwidth=2)
frame1.pack(side = LEFT,expand=NO,fill=None,padx=5)
frame1.pack_propagate(False)
frame2 = FrameDnd(Root,width=75, height = 400, GiveDropTo=TargetObject,relief=RAISED, borderwidth=2)
frame2.pack(side = LEFT,expand=NO,fill=None,padx=5)
frame2.pack_propagate(False)
frame3 = FrameDnd(Root,width=75, height = 400, GiveDropTo=TargetObject,relief=RAISED, borderwidth=2)
frame3.pack(side = LEFT,expand=NO,fill=None,padx=5)
frame3.pack_propagate(False)
frame4 = FrameDnd(Root,width=75, height = 400, GiveDropTo=TargetObject,relief=RAISED, borderwidth=2)
frame4.pack(side = LEFT,expand=NO,fill=None,padx=5)
frame4.pack_propagate(False)
frame5 = FrameDnd(Root,width=75, height = 400, GiveDropTo=TargetObject,relief=RAISED, borderwidth=2)
frame5.pack(side = LEFT,expand=NO,fill=None,padx=5)
frame5.pack_propagate(False)
frame6 = FrameDnd(Root,width=75, height = 400, GiveDropTo=TargetObject,relief=RAISED, borderwidth=2)
frame6.pack(side = LEFT,expand=NO,fill=None,padx=5)
frame6.pack_propagate(False)
frame7 = FrameDnd(Root,width=75, height = 400, GiveDropTo=TargetObject,relief=RAISED, borderwidth=2)
frame7.pack(side = LEFT,expand=NO,fill=None,padx=5)
frame7.pack_propagate(False)
frame8 = FrameDnd(Root,width=75, height = 400, GiveDropTo=TargetObject,relief=RAISED, borderwidth=2)
frame8.pack(side = LEFT,expand=NO,fill=None,padx=5)
frame8.pack_propagate(False)

frame_dict = {1:frame1,2:frame2,3:frame3,4:frame4,5:frame5,6:frame6,7:frame7,8:frame8}
# CommandOne = CanvasDnd(Root,GiveDropTo=TargetObject,relief=RAISED,bd=2)
# CommandOne.pack(side = LEFT,expand=YES,fill=BOTH)
# CommandTwo = CanvasDnd(Root,GiveDropTo=TargetObject,relief=RAISED,bd=2)
# CommandTwo.pack(side = LEFT,expand=NO,fill=BOTH)

Root.mainloop()
