import json
import re

from ibm_watson_machine_learning.foundation_models import Model


class RAGresponseGeneration:
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
        # set athentication credentials
        self.WXAPIkey    = WXAPIkey
        self.WXAPIurl    = WXAPIurl
        self.WXprojectID = WXprojectID
        self.WXdefaultModelID = "ibm/granite-13b-chat-v2"
        self.WXdefaultModelParams = {
            "decoding_method": "greedy",
            "max_new_tokens": 2000,
            "min_new_tokens": 0,
            "stop_sequences": ["\n\n"],
            "repetition_penalty": 1
        }

        self.WXmodel = self.setWXmodel( self.WXdefaultModelID, self.WXdefaultModelParams)
        return

    def setWXmodel(self, modelID, modelParams):
        credentials = {
            "url"    : self.WXAPIurl,
            "apikey" : self.WXAPIkey
        }
        self.WXmodel = Model( modelID, credentials, modelParams, self.WXprojectID )
        return self.WXmodel

    def promptWXmodel(self, promptTemplate, promptVariables):
        prompt = promptTemplate
        for varName, varValue in promptVariables.items():
            prompt = re.sub("{{" + varName + "}}", varValue, prompt)
        print(f'DEBUG: prompt: \n{prompt}')
        llmResponse = self.WXmodel.generate( prompt )
        print(llmResponse)
        if ( "results" in llmResponse ) and ( len( llmResponse["results"]) > 0 ) and ( "generated_text" in llmResponse["results"][0] ):
            generatedText = llmResponse["results"][0]["generated_text"]
            return generatedText.strip()
        else:
            print( "The model failed to generate an answer" )
            print( "\nDebug info:\n" + json.dumps( llmResponse, indent=3 ) )
            return ""

    # heler functions
    def getWXmodelDetails(self):
        modelDetails = self.WXmodel.get_details()
        modelParams  = self.WXmodel.params
        print(f'DEBUG: modelDetails: \n{json.dumps(modelDetails, indent=3)}')
        #print(f'Model name           : {modelDetails["label"]}')
        #print(f'Model id             : {modelDetails["model_id"]}')
        #print(f'Model context window : {modelDetails["model_limits"]["max_sequence_length"]}')
        #print(f'Model params         : {modelParams}')
        return {
            "modelName"          : modelDetails["label"],
            "modelId"            : modelDetails["model_id"],
            "modelContextWindow" : modelDetails["model_limits"]["max_sequence_length"],
            "modelParams"        : modelParams
        }

