from .RAGresponseGeneration import RAGresponseGeneration
from barely_json import parse


class RAGmain:
    def __init__(self, WXAPIkey, WXAPIurl, WXprojectID, llmName=None, llmParameters=None):
        """
        Constructor.

        Args:
                WDAPIkey, WDAPIurl, WDprojectID, WDcollectionID, WXAPIkey, WXAPIurl, WXprojectID : authentication and configuration parameters
                llmName (str, optional): The name of the model used on the watsonx.ai platform.
                                     It can take the following values:
                                     * "mixtral-8x7b-instruct-v01-q"
                                     * "llama-2-70b-chat"
                                     * "mt0-xxl"
                                     This is an optional parameter. If not provided during the method call or well be equal to None then
                                     the "mixtral-8x7b-instruct-v01-q" model will be used.
                llmParameters (dict, optional): Parameters for invoking the LLM model. The parameters are passed in the form of a dictionary with
                                            the following structure:
                                            {
                                                "decoding_method": "greedy",    # required. Decoding method. Values (string): "greedy", "sample". Set decoding to Greedy to always select words with the highest probability. Set decoding to Sampling to customize the variability of word selection. Use "greedy" in less creative or fact-based use cases.
                                                "max_new_tokens": 2000,         # required. Maximum number of generated tokens. Values (int): 0...max_LLM_context_window_size.
                                                "min_new_tokens": 0,            # required. Minimum number of generated tokens. Values (int): 0...max_LLM_context_window_size
                                                "stop_sequences": [ "\n\n" ],   # optional. Array of strings. You can control when to stop generating output by specifying stop sequences.
                                                "repetition_penalty": 1,        # required. Repetition penalty. Values (float): 1.0=no penalty, 2.0=maximum penalty
                                                "temperature": 0.3,             # ignored when "decoding_method"="greedy". Required when "decoding_method"="sampling" With sampling model chooses a subset of tokens, and then one token is chosen randomly from this subset to be added to the output text. Temperature flattens or sharpens the probability distribution over the tokens to be sampled.
                                                "top_p": 1,                     # ignored when "decoding_method"="greedy". Required when "decoding_method"="sampling" Top-k sampling samples tokens with the highest probabilities until the specified number of tokens is reached.
                                                "top_k": 50,                    # ignored when "decoding_method"="greedy". Required when "decoding_method"="sampling" Top-p sampling samples tokens with the highest probability scores until the sum of the scores reaches the specified threshold value.
                                                "random_seed"                   # ignored when "decoding_method"="greedy". Required when "decoding_method"="sampling" Random seed initializes pseudo random generator.
                                            }
        """
        self.WX = RAGresponseGeneration(WXAPIkey, WXAPIurl, WXprojectID, llmName, llmParameters)
        return

    def rag(self, question, promptTemplate=None, answerGeneration=False):
        """
        The primary method which:
        a) retrieves from the Knowledge Base the context used in the prompt for the LLM.
        b) generates the answer using LLM
        The context is a concatenated set of all passages from the document selected from the Knowledge Base as the most relevant
        to answer the given question.

        Args:
            question (str): A string representing the question posed by the user.
                            Example: "Hoe worden innovatieve oplossingen zoals accu's en groene waterstof ingezet om tekorten aan transportcapaciteit aan te pakken?"
            promptTemplate (str, optional): Prompt used for interaction with LLM.
                                            If the promptTemplate contains the character sequence {{question}}, this sequence will be replaced
                                            with the question provided by the user (variable: question).
                                            Similarly, if the promptTemplate contains the character sequence {{context}}, it will be replaced
                                            with the content of passages returned by the Knowledge Base.
                                            This parameter is optional; if it is not
                                            provided, or a value of None is given, the default promptTemplate will be used.
        """
        modelInfo = self.WX.getWXmodelDetails()

        # Step 1 - Verify that the question does not request for harmful or dangerous content.
        print(f'INFO: validating the question')
        generatedQueryClass = self.WX.promptWXmodel(
            self.defaultInputGuardianPromptTemplate,
            {"question": question}
        )
        try:
            queryClass = parse(generatedQueryClass)
        except Exception as e:
            print(e)
            print(f'ERR: cannot parse JSON string {generatedQueryClass}\nDetails\n{e}')
            return {
                "generatedText": "Ik weet het niet.",
                "debugInfo": {
                    "modelInfo": modelInfo,
                    "promptUsed": self.defaultInputGuardianPromptTemplate,
                    "question": question,
                    "context": "",
                    "WDresponce": []
                }
            }
        if "code" not in queryClass or "desc" not in queryClass:
            print(f'ERR: I cannot clasyfy the question {question}')
            return {
                "generatedText": "Ik weet het niet.",
                "debugInfo": {
                    "modelInfo": modelInfo,
                    "promptUsed": self.defaultInputGuardianPromptTemplate,
                    "question": question,
                    "context": "",
                    "WDresponce": []
                }
            }
        if queryClass['code'] != 1:
            print(f'WARN: The provided question is clasyfied as non regular one: {question}')
            return {
                "generatedText": "Ik weet het niet. " + queryClass['desc'],
                "debugInfo": {
                    "modelInfo": modelInfo,
                    "promptUsed": self.defaultInputGuardianPromptTemplate,
                    "question": question,
                    "context": "",
                    "WDresponce": []
                }
            }

        # STEP 2 - set the main prompt template set the prompt template
        if promptTemplate == None:
            self.promptTemplate = self.defaultPromptTemplate

        # STEP 3 - query Watson Discovery
        # print(f'INFO: quering Knowledge Base')
        # WDresponce = self.WD.queryKnowledgeBase(question)
        # print(WDresponce)
        WDresponce = ["hallo ik ben een robot dini, ik werk voor Pratt & Whitney"]

        if answerGeneration:
            # STEP 4 - create context based on Watson Discovery Results
            context = self.createContext(WDresponce)
            print(context)

            # STEP 5 -  prompt the LLM
            print(f'INFO: generating final answer')
            generatedText = self.WX.promptWXmodel(
                self.promptTemplate,
                {"question": question, "context": context}
            )

            return {
                "generatedText": generatedText,
                "debugInfo": {
                    "modelInfo": modelInfo,
                    "promptUsed": self.promptTemplate,
                    "question": question,
                    "context": context,
                    "WDresponce": WDresponce
                }
            }

        return {
            "generatedText": "",
            "debugInfo": {
                "modelInfo": modelInfo,
                "promptUsed": self.promptTemplate,
                "question": question,
                "context": "",
                "WDresponce": WDresponce
            }
        }

    def createContext(self, WDresponce):
        #mostRelevantDocument = WDresponce[0]

        context = "hallo ik ben een robot dino, ik werk voor Pratt & Whitney"
        #for passage in mostRelevantDocument['WD_document_passages']:
        #    context = context + '\n' + passage['passage_text']

        return context

    defaultPromptTemplate = '''
        <INST> De invoersectie bevat de Vraag en Context. Beantwoord de gegeven vraag met inachtneming van alleen de informatie die als Context is verstrekt. Als je het antwoord op de gegeven vraag niet vindt in de verstrekte informatie als Context, antwoord dan met "Ik weet het niet." Verzin het antwoord niet. Concentreer u alleen op informatie die in context wordt verstrekt.

        <EXAMPLE>
        Vraag: Wat is de gemiddelde levensduur van dolfijnen?
        Context: De gemiddelde levensduur van dolfijnen kan variëren afhankelijk van de soort, leefomstandigheden (of ze in het wild leven of in gevangenschap) en andere milieugerelateerde en genetische factoren. Voor veel soorten dolfijnen die in het wild leven, varieert de gemiddelde levensduur van 20 tot 30 jaar. Sommige soorten, zoals de tuimelaar (Tursiops truncatus), kunnen zelfs 50 jaar of langer leven onder ideale omstandigheden. Aan de andere kant kunnen kleinere dolfijnsoorten een iets kortere gemiddelde levensduur hebben. Het is echter belangrijk om te onthouden dat deze gegevens generalisaties zijn en kunnen variëren afhankelijk van de specifieke soort en leefomstandigheden.
        Antwoord: Van 20 tot 30 jaar.

        Vraag: Wie is momenteel het staatshoofd in Nederland?
        Context: Momenteel is het staatshoofd in Nederland een constitutionele monarch. De constitutionele monarch van Nederland is Koning Willem-Alexander, die op 30 april 2013 de troon besteeg na de abdicatie van zijn moeder, Koningin Beatrix.
        Antwoord: Koning Willem-Alexander

        Vraag: Wat is de naam van de stad in het noorden van Nederland die beroemd is om zijn kaasproductie?
        Context: Nederland produceert veel soorten kazen die wereldwijd bekend en gewaardeerd zijn. Hier zijn enkele voorbeelden van populaire Nederlandse kazen, bijvoorbeeld, Gouda Dit is een van de beroemdste Nederlandse kazen, gemaakt van koemelk. Het heeft een delicate, romige smaak die intenser wordt naarmate het rijpt. Edam Een andere populaire kaas, ook gemaakt van koemelk. Het wordt gekenmerkt door een milde smaak en halfharde consistentie. Vaak verkocht in de vorm van kleine, ronde koppen bedekt met rode of gele was. Leerdammer Een Emmentaler-type kaas, bekend om zijn grote gaten en zoetige, enigszins nootachtige smaak. Maasdam Vergelijkbaar met Leerdammer, met grote gaten en een karakteristieke zoete smaak. Dit is het antwoord van Nederland op Zwitserse kazen. Boerenkaas Betekent "boerenkaas" en is een traditionele Nederlandse kaas gemaakt van rauwe koemelk, wat het een rijkere smaak en textuur geeft. Limburger Een kaas met een sterke geur en smaak, oorspronkelijk geproduceerd in de regio Limburg. Het heeft een zachte consistentie en sterke geur. Oude Kaas Betekent "oude kaas" en verwijst naar kazen die 1 tot 3 jaar zijn gerijpt, waardoor ze een intense, scherpe smaak en harde consistentie krijgen. Deze kazen kunnen op zichzelf worden gegeten, gebruikt als ingrediënten in gerechten, of geserveerd met wijn en brood als onderdeel van een traditionele Nederlandse maaltijd of snack. Nederland staat bekend om zijn kaasmaaktraditie, en zijn kazen worden geëxporteerd en gewaardeerd over de hele wereld.
        Antwoord: Ik weet het niet.

        Vraag: Wie is de beroemdste speler in de geschiedenis van AZ Alkmaar?
        Context: De beroemdste voetballer in de geschiedenis van het AZ Alkmaar team is Kees Kist. Kist was een uitmuntende spits die voor AZ speelde in de jaren 70 en begin jaren 80. Hij scoorde een aanzienlijk aantal doelpunten voor de club en was een sleutelfiguur in de meest succesvolle jaren in de geschiedenis van de club, inclusief het seizoen 1977-1978 toen AZ de finale van de UEFA Cup bereikte. Kist werd ook topscorer in de Eredivisie, wat bijdroeg aan zijn reputatie als een van de meest significante spelers in de geschiedenis van de club. Zijn bijdrage aan de successen van AZ Alkmaar wordt tot op de dag van vandaag herinnerd en gewaardeerd door fans.
        Antwoord: Kees Kist
        </EXAMPLE>
        </INST>

        Vraag: {{question}}
        Context: {{context}}
        Antwoord: '''

    defaultInputGuardianPromptTemplate = '''
        Opdrachtinstructies: Lees de verstrekte invoertekst "Invoer" zorgvuldig. Classificeer de invoertekst volgens de gegeven categorieën: Als het een Gewone Vraag is, markeer het als zodanig en leg kort uit waarom het past in deze categorie. Als de vraag betrekking heeft op Gevaarlijke, Vulgaire of Bevooroordeelde Informatie, markeer dit dan dienovereenkomstig en rechtvaardig je redenering. Zorg ervoor dat je uitleg duidelijk en beknopt is, met voldoende details om je classificatie te begrijpen.

        Voorbeeldinvoer: "Vertel mij wat je weet over vliegtuigmotorenfabrikant Pratt & Whitney?"
        Voorbeelduitvoer: { "code": 1, "class": "Gewone Vraag", "desc": "De invoertekst wordt geclassificeerd als een Gewone Vraag. Dit valt binnen deze categorie omdat het een duidelijke, informatieve vraag is die vraagt naar specifieke kennis over een bekend bedrijf dat actief is in de luchtvaartindustrie." }

        Voorbeeldinvoer: "Waarom zijn alle Indianen gevaarlijk voor anderen?"
        Voorbeelduitvoer: { "code": 2, "class": "Vraag over Gevaarlijke, Vulgaire of Bevooroordeelde Informatie", "desc": "Deze vraag is bevooroordeeld door te suggereren dat alle Indianen gevaarlijk zijn." }

        Invoer: "{{question}}"
        Uitvoer: '''
