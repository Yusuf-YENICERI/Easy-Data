from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivy.uix.codeinput import CodeInput
from pygments.lexers.sql import MySqlLexer
from kivy.uix.popup import Popup
import time, MySql, re

class MainLayout(BoxLayout):
    pass

class SManager(ScreenManager):
    pass

class DynamicLabel(Label):
    pass

class EasyDataApp(App):

    ###Screen Start
    #Screen Manager Start
    sm = None
    #Screen Manager End

    ##Screen Code Start
    #Screen Code.Code Start
    codeInput = None
    #Screen Code.Code End
    ##Screen Code End

    ##Screen Process Parameters Start
    
    #Screen Process Code Start
    previousCodeInputObj = None
    previousCodeInput = None
    #Screen Process Code End
    
    #Screen Process TextInputs Start
    textInput = None
    tableName = None
    columnNumber = None
    #Screen Process TextInputs End

    ##Screen Process Parameters End
    
    ##Screen Database Parameters Start
    
    #Screen Database TextInputs Start
    databaseTextInput = None
    #Screen Database TextInputs End
    
    ##Screen Database Parameters End
    
    ##Screen Data Parameters Start
    dataInput = None
    previousDataInputObj = None
    previousDataInput = None

    ###Screen End
    #Database Connection Parameters Start
    db = None
    user = None
    password = None
    host = None
    dbName = None

    #Database Connection Parameters End
    
    #Database Functions Start
    def insertData(self, data):
        try:
            data = data.split("\n")
            self.ex("use " + EasyDataApp.dbName + ";", True)
            count = 0
            newData = []
            for i in data:
                i = re.sub("^ ", "", i)
                i = re.sub(" $", "", i)
                value = re.search("[a-zA-Z]", i)
                if value != None:
                    i = "\"" + i + "\""
                if i == "\n": continue
                count += 1
                newData.append(i)
                if count == int(EasyDataApp.columnNumber):
                    count = 0
                    EasyDataApp.db.insertData(newData)
                    newData = []
                    continue
        except Exception as e:
            self.messageBox("Pdften alınan veriler kısmında bir hata oluştu, lütfen her bir satıra bir veri koyun.", e)

    def makeTable(self, tableName, columns):
        try:
            self.ex("use " + EasyDataApp.dbName + ";", True)
            EasyDataApp.db.makeTable(tableName, columns)
            self.messageBox("İşlem başarıyla tamamlandı inşaallah.", None, "İşlem Sonucu")
        except Exception as e:
            self.messageBox("Tablo için verilen kolonlar oluşturulurken bir hata oluştu.", e)
    
    def recursiveExtract(self, thing):
        message = str()
        if not isinstance(thing, list):
            message += "\n"
        if isinstance(thing, (tuple, list)):
            for i in thing:
                if isinstance(i, (tuple,list)):
                    message += self.recursiveExtract(i)
                else:
                    message +=  str(i) + ", "
            return message
        else:
            return thing + ", "


    def ex(self, command, success_message = False ,**kwargs):
        try:
            newList = command.split(";")
            newList = [i for i in newList if re.search("[a-zA-Z]", i) != None]
            if newList[len(newList) - 1] == "":
                del newList[len(newList) - 1]
            for i in newList:
                i = i.replace("\n", "")
                i = i + ";"
                EasyDataApp.db.cursor.execute(i)
            
            results = EasyDataApp.db.cursor.fetchall()
            getMessage = self.recursiveExtract(results)
            self.messageBox(getMessage,None,"İşlem Sonucu")
        except Exception as e:
            if e.msg != "No result set to fetch from.":
                self.messageBox("Tablo için yazılan komutlar çalıştırılırken bir hata oluştu.", e)
            else:
                if success_message != True :
                    self.messageBox("İşlem başarıyla tamamlandı inşaallah.", None, "İşlem Sonucu")
               


    def makeDatabase(self):
        try:
            EasyDataApp.dbName = EasyDataApp.textInput[0].text
            if EasyDataApp.dbName != "":
                EasyDataApp.db.makeDatabase(EasyDataApp.dbName)
        except Exception as e:
            self.messageBox("Veri tabanı ismi oluşturulurken hata oluştu.",e)
    #Database Functions End

    ##Panel Functions Start
    def waitGoForScreenManager(self, dt):
        EasyDataApp.sm.current = "database"

    def openProcessPanel(self, instance):
        EasyDataApp.user = EasyDataApp.databaseTextInput[0].text
        EasyDataApp.password = EasyDataApp.databaseTextInput[1].text
        EasyDataApp.host = EasyDataApp.databaseTextInput[2].text
        try:
            EasyDataApp.db = MySql.MySql(**{
                                    "user" : str(EasyDataApp.user),
                                    "password" : str(EasyDataApp.password),
                                    "host" : str(EasyDataApp.host)
                            })
        except Exception as e:
            self.messageBox("Girilen verileri bir daha kontrol ediniz.", e)
            return
        
        EasyDataApp.sm.transition.direction = "left"
        EasyDataApp.sm.current = "process"

    def openCodePanel(self, instance):
        EasyDataApp.codeInput.text = EasyDataApp.previousCodeInputObj.text
        EasyDataApp.sm.transition.direction = "left"
        EasyDataApp.sm.current = "code"
    def closeCodePanel(self, instance):
        EasyDataApp.sm.transition.direction = "right"
        EasyDataApp.previousCodeInputObj.text = EasyDataApp.codeInput.text
        EasyDataApp.sm.current = "process"

    def openDataPanel(self, instance):
        EasyDataApp.dataInput.text = EasyDataApp.previousDataInputObj.text
        EasyDataApp.sm.transition.direction = "left"
        EasyDataApp.sm.current = "data"
    def closeDataPanel(self, instance):
        EasyDataApp.sm.transition.direction = "right"
        EasyDataApp.previousDataInputObj.text = EasyDataApp.dataInput.text
        EasyDataApp.sm.current = "process"
    ##Panel Functions End

    def processData(self, instance):
        self.makeDatabase()
        if EasyDataApp.textInput[1].text != "":
            EasyDataApp.tableName = EasyDataApp.textInput[1].text
        if EasyDataApp.textInput[2].text != "":
            EasyDataApp.columnNumber = EasyDataApp.textInput[2].text
        if EasyDataApp.textInput[3].text != "":
            EasyDataApp.previousCodeInput = EasyDataApp.textInput[3].text
            if EasyDataApp.tableName != None:                                                 #If all text inputs are filled  inshaALLAH
                self.makeTable(EasyDataApp.tableName, EasyDataApp.previousCodeInput)
                EasyDataApp.tableName = None
            else:                                                                           #If only command part is filled inshaALLAH
                self.ex(EasyDataApp.previousCodeInput)
                if EasyDataApp.previousCodeInput.find("insert") is not -1:
                    EasyDataApp.db.commit()
        if EasyDataApp.textInput[4].text != "":
            self.insertData(EasyDataApp.textInput[4].text)
     
    def messageBox(self, specialErrorMessage, e, title = None):
        specific_title = "Hata oluştu"
        if title != None:
            specific_title = title
        if specialErrorMessage.count("\n") > 9:
            warningMessage = "[color=fafafa][b] Görüntülemek istediğiniz bilgi 10 satırı aşıyor. Lütfen MySQL'in komut satırından bilgi alın. [/b][/color]"
            messageBox_warning = Popup(title="Uyarı", size_hint=(.5,.5))
            messageBox_warning.add_widget(Label(text=warningMessage, text_size=(messageBox_warning.size[0]*2, messageBox_warning.size[1]*2), font_size="16sp", markup = True, center=messageBox_warning.center, valign="center"))
            messageBox_warning.open()
        errorMessage = str()
        if e != None:
            errorMessage = "[color=fafafa][b]" + specialErrorMessage +  " Ayrıntılı bilgi: " + str(e) + "[/b][/color]"
        else:
            errorMessage = "[color=fafafa][b]" + specialErrorMessage +  "[/b][/color]"
        messageBox = Popup(title=specific_title, size_hint=(.5,.5))
        messageBox.add_widget(Label(text=errorMessage, text_size=(messageBox.size[0]*2, messageBox.size[1]*2), font_size="16sp", markup = True, center=messageBox.center, valign="center"))
        messageBox.open()

    def build(self):
        ##Process Page Start
        mainLayout = MainLayout(orientation="vertical")
        childLayouts = [BoxLayout(orientation="horizontal"), 
                        BoxLayout(orientation="horizontal"), 
                        BoxLayout(orientation="horizontal"),
                        BoxLayout(orientation="horizontal"),
                        BoxLayout(orientation="horizontal")]
        labels = [Label(text="[color=fafafa][b]Eski ya da oluşturulacak veri tabanı ismini girin:[/b][/color]", text_size = [300,50], font_size = "20sp", markup = True),
                  Label(text="[color=fafafa][b]Eski ya da oluşturulucak tablo ismini girin:[/b][/color]", text_size = [300, 50], font_size = "20sp", markup = True),
                  Label(text="[color=fafafa][b]Tablo için kolon sayısını girin:[/b][/color]", text_size = [300, 50], font_size = "20sp", markup = True),
                  Label(text="[color=fafafa][b]Tablo oluşturmak için kodları girin, ya da kolon isimlerini, aralarında virgül kullanarak girin:[/b][/color]", text_size = [300,100], font_size = "20sp", markup = True),
                  Label(text="[color=fafafa][b]Eklenecek verileri lütfen pdf'ten kopyalayın ve yapıştırın:[/b][/color]", text_size = [300, 50], font_size = "20sp", markup = True)]
        textInputs = [TextInput(multiline=False, background_color = [.31, .76, .97, 1], write_tab = False),
                      TextInput(multiline=False, background_color = [.31, .76, .97, 1], write_tab = False),
                      TextInput(multiline=False, background_color = [.31, .76, .97, 1], write_tab = False),
                      CodeInput(lexer=MySqlLexer(), auto_indent=True, background_color = [.31, .76, .97, 1]),   
                      TextInput(background_color = [.31, .76, .97, 1])]
        button_layout = BoxLayout(orientation="horizontal")
        firstButton = Button(text="[b][size=20sp]Veri Oluşturmak için Tam Ekran[/size][/b]", background_color = [.5,.5,.5,.5],markup=True)
        firstButton.bind(on_press=self.openDataPanel)
        secondButton = Button(text="[b][size=20sp]Tablo Oluşturmak için Tam Ekran[/size][/b]", background_color = [.5,.5,.5,.5],markup=True)
        secondButton.bind(on_press=self.openCodePanel)
        button_layout.add_widget(firstButton); 
        button_layout.add_widget(secondButton)
        mainLayout.add_widget(button_layout)
        lastButton = Button(text="[b][size=20sp]İşlemi Başlat[/size][/b]", background_color = [.5,.5,.5,.5],markup=True)
        lastButton.bind(on_press=self.processData)

        EasyDataApp.previousCodeInputObj = textInputs[3]
        EasyDataApp.previousDataInputObj = textInputs[4]
        

        #Add Widget Start
        add_multi_widget = lambda mLayout, layoutList: [mLayout.add_widget(i) for i in layoutList]
        add_multi_widget(mainLayout, childLayouts) #Add child layouts to main layout    
        add_multi_2widget = lambda cLayout, lbls, tInpts: [add_multi_widget(i,[k,m]) for (i,k,m) in zip(cLayout,lbls,tInpts)]
        add_multi_2widget(childLayouts, labels, textInputs) #Add widgets to child layout
        #Add Widget End

        ##Process Page End


        ##Screen Manager Start
        EasyDataApp.sm = SManager()

        screens = [Screen(name="opening"), Screen(name="process"),Screen(name="code"), Screen(name="database"), Screen(name="data")]
        #Screen Page 1 Start

        screens[0].add_widget(Label(text="[size=20][color=4caf50]Eser-ül[/size] [size=90]YENİÇERİ[/size][/color]", markup=True))
        
        #Screen Page 1 End
        
        #Screen Page 2 Start
        screens[1].add_widget(mainLayout)
        #Screen Page 2 End

        #Screen Page 3 Start
        EasyDataApp.codeInput = CodeInput(lexer=MySqlLexer(), auto_indent=True, background_color = [.31, .76, .97, 1],size_hint=(1,.9))
        acceptButton =  Button(text="[b][size=20sp]Tamam[/size][/b]", background_color = [.5,.5,.5,.5],markup=True,size_hint=(1,.1))
        acceptButton.bind(on_press=self.closeCodePanel)
        codeLayout = MainLayout(orientation="vertical")
        add_multi_widget(codeLayout, [EasyDataApp.codeInput, acceptButton])
        screens[2].add_widget(codeLayout)
        #Screen Page 3 End

        #Screen Page 4(database) Start
        databaseLayout = MainLayout(orientation="vertical")
        childDatabaseLayouts = [BoxLayout(orientation="horizontal",size_hint = (1, .26)), 
                        BoxLayout(orientation="horizontal", size_hint = (1, .26)), 
                        BoxLayout(orientation="horizontal", size_hint = (1, .26))]
        databaseLabels = [Label(text="[color=fafafa][b]Veri tabanı kullanıcı ismi:[/b][/color]", text_size = [300,50], font_size = "20sp", markup = True),
                  Label(text="[color=fafafa][b]Veri tabanı şifresi:[/b][/color]", text_size = [300, 50], font_size = "20sp", markup = True),
                  Label(text="[color=fafafa][b]Veri tabanının çalıştığı adres:[/b][/color]", text_size = [300,50], font_size = "20sp", markup = True)]
        EasyDataApp.databaseTextInput = databaseTextInputs = [TextInput(text="root", multiline=False, background_color = [.31, .76, .97, 1], write_tab = False),
                                                            TextInput(text="", multiline=False, background_color = [.31, .76, .97, 1], write_tab = False), 
                                                            TextInput(text="localhost", multiline=False, background_color = [.31, .76, .97, 1], write_tab = False)]
        databaseAcceptButton = Button(text="[b][size=20sp]Devam[/size][/b]", background_color = [.5,.5,.5,.5],markup=True, size_hint = (1, .2))
        databaseAcceptButton.bind(on_press = self.openProcessPanel)
        
        add_multi_widget(databaseLayout, childDatabaseLayouts)
        add_multi_2widget(childDatabaseLayouts, databaseLabels, databaseTextInputs)

        databaseLayout.add_widget(databaseAcceptButton)

        screens[3].add_widget(databaseLayout)
        #Screen Page 4(database) End

        #Screen Page 5(data) Start
        EasyDataApp.dataInput = CodeInput(lexer=MySqlLexer(), auto_indent=True, background_color = [.31, .76, .97, 1],size_hint=(1,.9))
        acceptButton_data =  Button(text="[b][size=20sp]Tamam[/size][/b]", background_color = [.5,.5,.5,.5],markup=True,size_hint=(1,.1))
        acceptButton_data.bind(on_press=self.closeDataPanel)
        dataLayout = MainLayout(orientation="vertical")
        add_multi_widget(dataLayout, [EasyDataApp.dataInput, acceptButton_data])
        screens[4].add_widget(dataLayout)
        #Screen Page 5(data) End

        add_multi_widget(EasyDataApp.sm, screens)

        EasyDataApp.sm.current = "opening"
        
        Clock.schedule_once(self.waitGoForScreenManager, 20)
        ##Screen Manager End

        mainLayout.add_widget(lastButton)

        EasyDataApp.textInput = textInputs
        return EasyDataApp.sm

EasyDataApp().run()

