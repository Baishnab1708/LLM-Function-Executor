import requests
import speech_recognition as sr
import pyttsx3
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)


class VoiceAutomationTester:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()

        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 0.9)

        # Voice settings
        self.wake_word = "computer"
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    def speak(self, text):
        """Convert text to speech"""
        print(f"{Fore.BLUE}🔊 {text}")
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except:
            pass

    def listen_for_wake_word(self):
        """Listen for wake word continuously"""
        print(f"{Fore.CYAN}🎤 Listening for wake word '{self.wake_word}'...")
        print(f"{Fore.YELLOW}Say '{self.wake_word}' followed by your command")
        print(f"{Fore.CYAN}Press Ctrl+C to exit")

        # Adjust for ambient noise once
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except:
            pass

        while True:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)

                try:
                    text = self.recognizer.recognize_google(audio, language='en-US').lower()
                    print(f"{Fore.GREEN}🎤 Heard: {text}")

                    # Check for wake word
                    if self.wake_word in text:
                        command = text.split(self.wake_word, 1)[-1].strip()
                        if command:
                            self.process_voice_command(command)
                        else:
                            self.speak("I'm listening, what would you like me to do?")
                            self.listen_for_command()

                    # Check for exit commands
                    elif any(word in text for word in ["exit", "quit", "stop", "goodbye"]):
                        self.speak("Goodbye!")
                        break

                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    print(f"{Fore.RED}Recognition service error")
                    continue

            except sr.WaitTimeoutError:
                continue
            except KeyboardInterrupt:
                print(f"\n{Fore.CYAN}Stopping...")
                break

    def listen_for_command(self):
        """Listen for a single command after wake word"""
        print(f"{Fore.CYAN}🎤 Listening for command...")

        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=8)

            command = self.recognizer.recognize_google(audio, language='en-US')
            print(f"{Fore.GREEN}🎤 Command: {command}")
            self.process_voice_command(command)

        except sr.UnknownValueError:
            self.speak("Sorry, I didn't understand that.")
        except sr.RequestError:
            self.speak("Recognition service error.")
        except sr.WaitTimeoutError:
            self.speak("I didn't hear anything.")

    def process_voice_command(self, command):
        """Process the voice command"""
        print(f"{Fore.YELLOW}Processing: {command}")

        # Handle help commands
        if "what can you do" in command.lower() or "help" in command.lower():
            response = "I can open applications, check system info, manage processes, run commands, and more."
            self.speak(response)
            return

        # Execute the command
        self.execute_command(command)

    def execute_command(self, prompt):
        """Execute command via API"""
        try:
            response = self.session.post(
                f"{self.base_url}/execute",
                json={"prompt": prompt},
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                function_name = result.get('function', 'Unknown')
                output = result.get('output', 'No output')

                print(f"{Fore.GREEN}✓ Success: {function_name}")
                print(f"{Fore.WHITE}Output: {output}")

                # Speak the result
                self.speak(f"Command executed. {output}")

            else:
                error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
                error_msg = error_data.get('error', 'Unknown error')
                print(f"{Fore.RED}✗ Error: {error_msg}")
                self.speak(f"Error: {error_msg}")

        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}✗ Connection failed - Is the server running?")
            self.speak("Connection failed. Please check if the server is running.")
        except requests.exceptions.Timeout:
            print(f"{Fore.RED}✗ Request timeout")
            self.speak("Request timed out.")
        except Exception as e:
            print(f"{Fore.RED}✗ Error: {e}")
            self.speak("An error occurred.")

    def check_server_health(self):
        """Check if server is responsive"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def test_voice_setup(self):
        """Test voice recognition and TTS"""
        print(f"{Fore.CYAN}Testing voice setup...")

        # Test TTS
        self.speak("Voice system initialized.")

        # Test microphone
        print(f"{Fore.YELLOW}Testing microphone - say something within 5 seconds...")
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)

            text = self.recognizer.recognize_google(audio, language='en-US')
            print(f"{Fore.GREEN}✓ Microphone test passed. You said: {text}")
            self.speak(f"I heard you say: {text}")
            return True

        except sr.UnknownValueError:
            print(f"{Fore.RED}✗ Could not understand audio")
            self.speak("Microphone is working but couldn't understand.")
            return True
        except sr.WaitTimeoutError:
            print(f"{Fore.RED}✗ No audio detected")
            self.speak("No audio detected. Please check your microphone.")
            return False
        except:
            print(f"{Fore.RED}✗ Voice test failed")
            return False

    def run(self):
        """Main entry point"""
        print(f"{Fore.CYAN}{'=' * 50}")
        print(f"{Fore.CYAN}    VOICE AUTOMATION SYSTEM")
        print(f"{Fore.CYAN}{'=' * 50}")

        # Check server health
        if not self.check_server_health():
            print(f"{Fore.RED}⚠️  Server is not responding at {self.base_url}")
            print(f"{Fore.YELLOW}Make sure the Flask app is running first!")
            return

        print(f"{Fore.GREEN}✓ Server is healthy")

        # Test voice setup
        if not self.test_voice_setup():
            print(f"{Fore.RED}Voice setup failed. Please check your microphone.")
            return

        print(f"{Fore.GREEN}✓ Voice system ready")

        # Start voice recognition
        self.speak("Voice automation system is ready. Say computer followed by your command.")

        print(f"\n{Fore.CYAN}Available Commands:")
        print(f"{Fore.WHITE}• Open applications: 'Computer, open calculator/chrome/notepad'")
        print(f"{Fore.WHITE}• System info: 'Computer, get CPU usage/RAM usage/system info'")
        print(f"{Fore.WHITE}• Process management: 'Computer, list processes/kill chrome'")
        print(f"{Fore.WHITE}• File operations: 'Computer, open file explorer/create file test.txt'")
        print(f"{Fore.WHITE}• System control: 'Computer, shutdown/restart system'")
        print(f"{Fore.WHITE}• Shell commands: 'Computer, run dir' (or any command)")
        print(f"{Fore.WHITE}• Help: 'Computer, what can you do'")
        print(f"{Fore.WHITE}• Exit: 'Exit' or 'Quit' to stop")
        print()

        try:
            self.listen_for_wake_word()
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Shutting down...")
            self.speak("Voice system shutting down.")


def main():
    print(f"{Fore.CYAN}Initializing Voice Automation System...")

    try:
        tester = VoiceAutomationTester()
        tester.run()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        print(f"{Fore.YELLOW}Please install required packages:")
        print(f"{Fore.WHITE}pip install SpeechRecognition pyttsx3 pyaudio colorama requests")


if __name__ == "__main__":
    main()