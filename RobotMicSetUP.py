class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self, False)
        self.filepath = ""
        self.sample_rate = 16000
        self.channels = (0, 0, 1, 0)  # pouze přední mikrofon

    def onLoad(self):
        try:
            self.ad = self.session().service("ALAudioDevice")
            self.ar = self.session().service("ALAudioRecorder")
        except Exception as e:
            self.ad = None
            self.logger.error(e)
        self.bIsRecording = False
        self.bIsRunning = False

    def onUnload(self):
        self.bIsRunning = False
        if self.bIsRecording:
            self.ar.stopMicrophonesRecording()
            self.bIsRecording = False

    def onInput_onStart(self, p):
        if self.bIsRunning:
            return
        self.bIsRunning = True
        sExtension = self.toExtension(self.getParameter("Microphones used"))
        self.filepath = p + sExtension
        if self.ad:
            # Spuštění nahrávání s požadovanými parametry
            self.ar.startMicrophonesRecording(self.filepath,"wav", self.sample_rate, self.channels)
            self.bIsRecording = True
        else:
            self.logger.warning("No sound recorded")

    def onInput_onStop(self):
        if self.bIsRunning:
            self.onUnload()
            print(self.filepath)
            self.onStopped(self.filepath)

    def toExtension(self, sMicrophones):
        if sMicrophones == "Front head microphone only (.ogg)":
            return ".ogg"
        else:
            return ".wav"
