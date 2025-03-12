from data.genericData import genericLinks

class GenericInfo:
    def getGenericInfo(self,payload):
        generic_data_info=payload['queryResult']['parameters']['GenericInfo']
        return f""" The below link should help you out with your request
        {genericLinks[generic_data_info]}
        """

