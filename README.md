# QA_taln
 Ce projet a été réalisé sous forme de suite de travaux pratiques le but étant de réaliser un système de questions réponses en langue naturelle sur des données structurées.
 Utilisation de la librairie Spacy pour retrouver les entités nommées et la tokenization des questions en entrées du système. NLTK pour calculer la distance de Levenshtein entre les tokens d'une questions et les relations pour trouver la plus proche.
 
 # Documentation
 Le programme commence d'abord par extraire les questions en Anglais dans le fichier questions.xml afin de les traiter. La première étape du traitement consiste à essayer de trouver quel est le type de réponse à la question (personne, organisation, lieu ...) à l'aide du pronom en début et du contexte. Dans un second temps, on récupère l'entité nommée de la question à l'aide de la librairie Spacy et la relation en comparant les tokens de la phrase avec les relations fournis dans le fichier relations.xml afin de requêter la base de données DBpedia. Quand on dispose de ces deux informations qui sont une condition nécessaire, on passe à l'étape de la préparation et d'envoi de la requête vers DBpedia pour récupérer les réponses possibles aux questions traitées. Enfin, on analyse les résultats avec différentes métriques pour évaluer le système mis en place.
 
 - Remarques et évolution possibles :

En souhaitant améliorer les résultats des requêtes ou affiner la recherche d'entité nommée, on peut utiliser des regex sur nos questions en entrée. Le souci serait de spécifier sur un jeu de données précis en entrée certes en améliorant les résultats pour celui-ci mais en perdant la robustesse et la capacité de généralisation du système on changeant les questions. J'ai donc fait le choix de ne pas utiliser de regex pour cette raison.

L'algorithme de recherche de relations peut être amélioré, car certaines relations ne sont pas comparées avec les bon tokens ou la relation diffère des tokens de la phrase ce qui amène à des erreurs. D'autres approches algorithmiques différent de la distance de Levenshtein peuvent permettre de résoudre ce problème. 
 
  # Utilisation
 - Librairies nécessaires :

math  
re  
nltk  
spacy  
SPARQLWrapper   
lxml  

 - Fichiers nécessaires :

relations.xml -> contiens les différentes relations possibles  
questions.xml -> contiens les questions et les réponses (URI DBpedia) attendues.  
 
