import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


news=[{"id":1,"content":"WASHINGTON Swedish furniture company IKEA Group [IKEA.UL] is recalling almost 36 million chests and dressers in the United States and Canada but said the products linked to the deaths of six children are safe when anchored to walls as instructed.\n\nThe recall covers six models of MALM chests or dressers manufactured from 2002 to 2016 and about 100 other families of chests or dressers that the U.S. Consumer Product Safety Commission said could topple over if not anchored securely to walls, posing a threat to children.\n\n\"It is simply too dangerous to have the recalled furniture in your home unanchored, especially if you have young children,\" CPSC Chairman Elliott Kaye said in a statement on Tuesday.\n\nTipped-over furniture or television sets kill a U.S. child every two weeks, he added.\n\nIKEA said that the recall was based on a standard applicable in North America for free-standing clothing storage units and that the products meet all mandatory stability requirements in Europe and other parts of the world.\n\n\"When attached to a wall the products are safe. We have had no other issues with that in any other country,\" said Kajsa Johansson, a spokeswoman for IKEA in Sweden.\n\nIKEA said it had no details on potential costs stemming from the recall.\n\nA recall summary from the company said that the chests and dressers are unstable if not properly anchored to a wall, posing a serious tip-over and entrapment hazard that could result in death or injury to children.\n\nTwo U.S. toddlers died in separate 2014 incidents when MALM chests fell on them. A 22-month-old boy was killed last year in a similar incident, which occurred after IKEA had announced a repair program including a free wall-anchoring kit.\n\nNone of the furnishings in the fatal incidents had been anchored to a wall.\n\nIKEA had received reports of 41 tip-over incidents involving non-MALM chests that caused 19 injuries and the deaths of three children from 1989 to 2007.\n\nAs part of the recall, IKEA is offering refunds or a free wall-anchoring kit.\n\nThe U.S. recall covers about 8 million MALM chests and dressers and 21 million other models of chests and dressers. About 6.6 million are being recalled in Canada.\n\nIkea has sold approximately 147.4 million chests of drawers globally since 1998.\n\n(Reporting by Ian Simpson in Washington DC and Mia Shanley in Stockholm; Editing by Dan Grebler and David Goodman)"
},{"id":2,"content":"Photo\n\nIn a deal with federal regulators, Ikea announced Tuesday that it would recall 29 million chests and dressers in the United States after at least six toddlers were crushed to death in tip-over accidents.\n\nThe move by the Swedish company, the world’s largest furniture seller, represented a crucial victory for consumer advocates in a yearslong effort to hold it accountable for a growing death toll of young children dating to 1989.\n\nThe head of the Consumer Product Safety Commission issued a stark warning to owners of furniture included in the recall.\n\n“If you have or think you have one of these products, act immediately,” the commission’s chairman, Elliot F. Kaye, said in a statement. “It is simply too dangerous to have the recalled furniture in your home unanchored, especially if you have young children.”\n\nAlan M. Feldman, a Philadelphia lawyer who is representing three of the families of toddlers in lawsuits against Ikea, said he welcomed the recall, but wished it had been issued much sooner. (He also said that the commission on Tuesday failed to note the death of a 3-year-old girl that was blamed on Ikea furniture in 2005, raising the toll to at least seven).\n\nAdvertisement Continue reading the main story\n\n“I don’t think that we should forget that it took seven deaths and more than 70 injuries and an untold number of near-misses before Ikea was shamed into taking action,” Mr. Feldman said.\n\nLars Petersson, the president and chief executive of Ikea USA, said the recalled furniture was never intended to be free-standing, but rather secured to walls with provided straps, a step he called “an integral part of the assembly instructions.”\n\n“If you are assembling correctly, the product is actually a very safe product,” he said in an interview on Tuesday.\n\nMr. Petersson declined to comment on the lawsuits brought by families, which accuse the company of knowing about the deadly risks of its furniture and failing to do anything about it.\n\nGet the Morning Briefing by Email What you need to know to start your day, delivered to your inbox. Monday – Friday.\n\n“The death of a child is an incredible loss,” he said. “It should never happen. So our hearts go out to the families that have to go through this.”\n\nA child dies, on average, once every two weeks in accidents that involve the toppling of furniture or bulky television sets, according to the safety commission. Every year, about 38,000 people visit emergency rooms for injuries related to tip-over accidents, a majority involving children under 5.\n\nIn many cases, the children slide drawers out from a dresser and then try to climb them like stairs. In a moment, an everyday item becomes lethal.\n\nThe commission said all six of the children crushed to death by Ikea furniture were 3 years old or younger. It also received reports of 36 injuries to children, it said.\n\nAdvertisement Continue reading the main story\n\nIkea’s recall applies to eight million chests and drawers in the company’s popular Malm line, the style involved in each of the last three deaths from 2014 to 2016.\n\nThe latest case, in February, added new urgency to the recall campaign. According to police records obtained by Philly.com, a woman in Minnesota went into her toddler’s bedroom to check on him during a nap and found him crushed beneath a six-drawer Malm dresser. Emergency medical workers were unable to revive him.\n\nMost American furniture manufacturers adhere to voluntary safety standards, which ensure that a unit will not tip over when a drawer is extended and 50 pounds of weight is applied. The recall on Tuesday applies to all Ikea furniture that fails that test, the commission said.\n\nLast summer, Ikea offered free wall anchor kits to owners of its furniture, a step that consumer advocates dismissed as inadequate given that many consumers were unaware of the dangers posed by unsecured furniture.\n\nAs part of the agreement on Tuesday, Ikea agreed to pick up the recalled furniture from customers’ homes and issue a refund, or to install an anchor that secures them to the wall. It also applies to customers in Canada, where a 6.6 million units of the recalled furniture was sold.\n\nMr. Kaye, the safety commission chairman, said on Tuesday that he was encouraged by Ikea’s willingness make changes, adding, “That doesn’t exonerate them from the past, but it is, from a consumer-safety standpoint, a positive announcement.”\n\nAsked whether any other retailers were selling furniture that posed risks to children, he said"}]


contents=[]
ID=[]
j=0 #store tha value of the number of documents 

#Extract raw descriptions and the corresponding two class labels for those descriptions
for item in news:
    contents.append(item["content"])
    ID.append(item["id"])
    j=j+1

#list of news   
#news=["WASHINGTON Swedish furniture company IKEA Group [IKEA.UL] is recalling almost 36 million chests and dressers in the United States and Canada but said the products linked to the deaths of six children are safe when anchored to walls as instructed.\n\nThe recall covers six models of MALM chests or dressers manufactured from 2002 to 2016 and about 100 other families of chests or dressers that the U.S. Consumer Product Safety Commission said could topple over if not anchored securely to walls, posing a threat to children.\n\n\"It is simply too dangerous to have the recalled furniture in your home unanchored, especially if you have young children,\" CPSC Chairman Elliott Kaye said in a statement on Tuesday.\n\nTipped-over furniture or television sets kill a U.S. child every two weeks, he added.\n\nIKEA said that the recall was based on a standard applicable in North America for free-standing clothing storage units and that the products meet all mandatory stability requirements in Europe and other parts of the world.\n\n\"When attached to a wall the products are safe. We have had no other issues with that in any other country,\" said Kajsa Johansson, a spokeswoman for IKEA in Sweden.\n\nIKEA said it had no details on potential costs stemming from the recall.\n\nA recall summary from the company said that the chests and dressers are unstable if not properly anchored to a wall, posing a serious tip-over and entrapment hazard that could result in death or injury to children.\n\nTwo U.S. toddlers died in separate 2014 incidents when MALM chests fell on them. A 22-month-old boy was killed last year in a similar incident, which occurred after IKEA had announced a repair program including a free wall-anchoring kit.\n\nNone of the furnishings in the fatal incidents had been anchored to a wall.\n\nIKEA had received reports of 41 tip-over incidents involving non-MALM chests that caused 19 injuries and the deaths of three children from 1989 to 2007.\n\nAs part of the recall, IKEA is offering refunds or a free wall-anchoring kit.\n\nThe U.S. recall covers about 8 million MALM chests and dressers and 21 million other models of chests and dressers. About 6.6 million are being recalled in Canada.\n\nIkea has sold approximately 147.4 million chests of drawers globally since 1998.\n\n(Reporting by Ian Simpson in Washington DC and Mia Shanley in Stockholm; Editing by Dan Grebler and David Goodman)",
#     "Photo\n\nIn a deal with federal regulators, Ikea announced Tuesday that it would recall 29 million chests and dressers in the United States after at least six toddlers were crushed to death in tip-over accidents.\n\nThe move by the Swedish company, the world’s largest furniture seller, represented a crucial victory for consumer advocates in a yearslong effort to hold it accountable for a growing death toll of young children dating to 1989.\n\nThe head of the Consumer Product Safety Commission issued a stark warning to owners of furniture included in the recall.\n\n“If you have or think you have one of these products, act immediately,” the commission’s chairman, Elliot F. Kaye, said in a statement. “It is simply too dangerous to have the recalled furniture in your home unanchored, especially if you have young children.”\n\nAlan M. Feldman, a Philadelphia lawyer who is representing three of the families of toddlers in lawsuits against Ikea, said he welcomed the recall, but wished it had been issued much sooner. (He also said that the commission on Tuesday failed to note the death of a 3-year-old girl that was blamed on Ikea furniture in 2005, raising the toll to at least seven).\n\nAdvertisement Continue reading the main story\n\n“I don’t think that we should forget that it took seven deaths and more than 70 injuries and an untold number of near-misses before Ikea was shamed into taking action,” Mr. Feldman said.\n\nLars Petersson, the president and chief executive of Ikea USA, said the recalled furniture was never intended to be free-standing, but rather secured to walls with provided straps, a step he called “an integral part of the assembly instructions.”\n\n“If you are assembling correctly, the product is actually a very safe product,” he said in an interview on Tuesday.\n\nMr. Petersson declined to comment on the lawsuits brought by families, which accuse the company of knowing about the deadly risks of its furniture and failing to do anything about it.\n\nGet the Morning Briefing by Email What you need to know to start your day, delivered to your inbox. Monday – Friday.\n\n“The death of a child is an incredible loss,” he said. “It should never happen. So our hearts go out to the families that have to go through this.”\n\nA child dies, on average, once every two weeks in accidents that involve the toppling of furniture or bulky television sets, according to the safety commission. Every year, about 38,000 people visit emergency rooms for injuries related to tip-over accidents, a majority involving children under 5.\n\nIn many cases, the children slide drawers out from a dresser and then try to climb them like stairs. In a moment, an everyday item becomes lethal.\n\nThe commission said all six of the children crushed to death by Ikea furniture were 3 years old or younger. It also received reports of 36 injuries to children, it said.\n\nAdvertisement Continue reading the main story\n\nIkea’s recall applies to eight million chests and drawers in the company’s popular Malm line, the style involved in each of the last three deaths from 2014 to 2016.\n\nThe latest case, in February, added new urgency to the recall campaign. According to police records obtained by Philly.com, a woman in Minnesota went into her toddler’s bedroom to check on him during a nap and found him crushed beneath a six-drawer Malm dresser. Emergency medical workers were unable to revive him.\n\nMost American furniture manufacturers adhere to voluntary safety standards, which ensure that a unit will not tip over when a drawer is extended and 50 pounds of weight is applied. The recall on Tuesday applies to all Ikea furniture that fails that test, the commission said.\n\nLast summer, Ikea offered free wall anchor kits to owners of its furniture, a step that consumer advocates dismissed as inadequate given that many consumers were unaware of the dangers posed by unsecured furniture.\n\nAs part of the agreement on Tuesday, Ikea agreed to pick up the recalled furniture from customers’ homes and issue a refund, or to install an anchor that secures them to the wall. It also applies to customers in Canada, where a 6.6 million units of the recalled furniture was sold.\n\nMr. Kaye, the safety commission chairman, said on Tuesday that he was encouraged by Ikea’s willingness make changes, adding, “That doesn’t exonerate them from the past, but it is, from a consumer-safety standpoint, a positive announcement.”\n\nAsked whether any other retailers were selling furniture that posed risks to children, he said"]

def lemma_tokenizer(text):
    # use the standard scikit-learn tokenizer first to converting strings of descriptions to a list of tokens
    standard_tokenizer = TfidfVectorizer().build_tokenizer()
    tokens = standard_tokenizer(text)
    # then use NLTK to perform lemmatisation on each token
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemma_tokens = []
    for token in tokens:
        lemma_tokens.append( lemmatizer.lemmatize(token) )
    return lemma_tokens

#turn the corpus content into numerical feature vectors to help make classify
#TfidfVectorizer is equal to CountVectorizer followed by TfidfTransformer
vectorizer = TfidfVectorizer(stop_words="english",lowercase=True,min_df = 2,tokenizer=lemma_tokenizer)

#Learn vocabulary and idf and Transform documents to document-term matrix.
X = vectorizer.fit_transform(contents)
print(X.shape)
#print(X)
#print(X[1])

terms=vectorizer.get_feature_names()
print(terms)

a1=X.toarray()

indices1 = np.argsort(a1[0])[::-1]
indices2 = np.argsort(a1[1])[::-1]

features = vectorizer.get_feature_names()
top_n = 20
top_features1 = [features[i] for i in indices1[:top_n]]
print(top_features1)

top_features2 = [features[i] for i in indices2[:top_n]]
print(top_features2)


#join two lists together
in_first = set(top_features1)
in_second = set(top_features2)

in_second_but_not_in_first = in_second - in_first

result = top_features1 + list(in_second_but_not_in_first)
print (result)




#lemmatizer = WordNetLemmatizer()

#for w in contents[0].split(' '):
#    print( lemmatizer.lemmatize(w).lower() )

#for w in contents[0].split(' '):
#    print( lemmatizer.lemmatize(w).lower() )
    
def get_all_word_counts(wordunion,content):
    intial_words=content.split(' ')
    words=[] #
    filtered_words = [word for word in intial_words if word not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    for w in filtered_words:
        new_w=lemmatizer.lemmatize(w).lower()
        words.append(new_w)
    word_counts=dict((el,0) for el in wordunion)
    for word in words:
        if word in word_counts:     #If not already there
            word_counts[word]+=1          #Increment the count accordingly
    return word_counts

#d1=dict((el,0) for el in result)
d1=get_all_word_counts(result,contents[0])
d2=get_all_word_counts(result,contents[1])
print(d1)
print(d2)   

from sklearn.metrics.pairwise import cosine_similarity
print(cosine_similarity(list(d1.values()),list(d2.values())))