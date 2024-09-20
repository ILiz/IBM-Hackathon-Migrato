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

    def rag(self, question, context, promptTemplate=None, answerGeneration=False):
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

        if promptTemplate is None:
            self.promptTemplate = self.defaultPromptTemplate

        if answerGeneration:
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
                    "context": context
                }
            }

        return {
            "generatedText": "",
            "debugInfo": {
                "modelInfo": modelInfo,
                "promptUsed": self.promptTemplate,
                "question": question,
                "context": ""
            }
        }

    defaultPromptTemplate = '''
        <INST> The input contains Question and Context. Answer the given Question using only knowledge from the given Context. If the answer is not in the given Context, the Answer is "I cannot help you with that, reformulate your question." Do not create your answer. Only focus on the given Context.

        <EXAMPLE>
        Question: When did World War I start?
        Context: World War I or the First World War (28 July 1914 – 11 November 1918), also known as the Great War, was a global conflict between two coalitions: the Allies (or Entente) and the Central Powers. Fighting took place mainly in Europe and the Middle East, as well as in parts of Africa and the Asia-Pacific, and in Europe was characterised by trench warfare and the use of artillery, machine guns, and chemical weapons (gas). World War I was one of the deadliest conflicts in history, resulting in an estimated 9 million military dead and 23 million wounded, plus up to 8 million civilian deaths from causes including genocide (including the Armenian genocide). The movement of large numbers of people was a major factor in the Spanish flu pandemic, which killed millions.
        Answer: World War I start on 28 July 1914.

        Question: Explain cognitive dissonance.
        Context: In the field of psychology, cognitive dissonance is described as the mental disturbance people feel when they realize their cognitions and actions are inconsistent or contradictory. This may ultimately result in some change in their cognitions or actions to cause greater alignment between them so as to reduce this dissonance. Relevant items of information include peoples' actions, feelings, ideas, beliefs, values, and things in the environment. Cognitive dissonance is typically experienced as psychological stress when persons participate in an action that goes against one or more of those things. According to this theory, when an action or idea is psychologically inconsistent with the other, people do all in their power to change either so that they become consistent. The discomfort is triggered by the person's belief clashing with new information perceived, wherein the individual tries to find a way to resolve the contradiction to reduce their discomfort.
        Answer: Cognitive dissonane is descrives as the mental disturbance people feel when they realice their cognitions and actions are inconsistent or contradictory.

        Question: Give me a question about the Mona Lisa.
        Context: The Mona Lisa painting is one of the most emblematic portraits in the history of art, where is located at the Louvre. Painted by Leonardo da Vinci in the 16th century, it joined the collections of the court of France before being added to the works on display at the Louvre Museum
        Answer: Who painted the Mona Lisa? (Leonardo da Vinci)
        </EXAMPLE>
        </INST>

        Question: {{question}}
        Context: {{context}}
        Answer: '''
