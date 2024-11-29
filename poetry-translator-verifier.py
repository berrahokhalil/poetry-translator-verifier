import streamlit as st
from deep_translator import GoogleTranslator
import ply.lex as lex
import ply.yacc as yacc
import speech_recognition as sr
import difflib




# ======================================
# Données des poèmes
# ======================================

french_poems = [
    "Les sanglots longs des violons de l’automne.",
    "Sur mes cahiers d’écolier Sur mon pupitre et les arbres Sur le sable sur la neige J’écris ton nom : Liberté.",
    "Sous le pont Mirabeau coule la Seine Et nos amours, Faut-il qu’il m’en souvienne La joie venait toujours après la peine.",
    "Demain, dès l’aube, à l’heure où blanchit la campagne, Je partirai. Vois-tu, je sais que tu m’attends. J’irai par la forêt, j’irai par la montagne.",
    "Je fais souvent ce rêve étrange et pénétrant D’une femme inconnue, et que j’aime, et qui m’aime.",
    "Il pleure dans mon cœur Comme il pleut sur la ville. Quelle est cette langueur Qui pénètre mon cœur ?",
    "Par les soirs bleus d’été, j’irai dans les sentiers, Picoté par les blés, fouler l’herbe menue.",
    "Heureux qui, comme Ulysse, a fait un beau voyage, Ou comme cestuy-là qui conquit la toison.",
    "Un éclair… puis la nuit ! — Fugitive beauté Dont le regard m’a fait soudainement renaître.",
    "Souvent, pour s’amuser, les hommes d’équipage Prennent des albatros, vastes oiseaux des mers."
]

arabic_poems = [
    "وأنتَ بعيدٌ عن عينيَّ أراكَ قريبا من قلبي كأنك نبضي الذي يتسللُ في شراييني.",
    "إذا المرءُ لم يُدنَسْ مِنَ اللؤمِ عِرضُهُ فكلُّ رِداءٍ يَرتديهِ جميلُ.",
    "قال: السماء كئيبة وتجهما قلت: ابتسم يكفي التجهم في السما.",
    "تعالَ لنسبحَ في ضوء القمر، ونطيرَ في فضاءِ الأحلام.",
    "عيناكِ غابتا نخيلٍ ساعةَ السحَرْ أو شُرفتان راح ينأى عنهما القمرْ.",
    "لا تقف على الأطلال ولا تسأل عن الماضي، فالحياة تمضي وما ذهب، لا يعود.",
    "أراكَ عصيَّ الدمعِ شيمتُكَ الصبرُ أما للهوى نهيٌ عليكَ ولا أمرُ؟",
    "غريبٌ أنا في هذا العالم، غريبٌ كنجمةٍ بعيدة تضيء ولا تنطفئ.",
    "إذا سبَّني نذلٌ تزايدتُ رفعةً وما العيبُ إلّا أن أكونَ مُسابِبَا.",
    "أحبكِ أكثر من كلامي، من صمتي، ومن نظراتي العابرة."
]

english_poems = [
    "Some say the world will end in fire, Some say in ice.",
    "Hope is the thing with feathers - That perches in the soul - And sings the tune without the words - And never stops - at all.",
    "She walks in beauty, like the night Of cloudless climes and starry skies.",
    "All that we see or seem Is but a dream within a dream.",
    "Nature’s first green is gold, Her hardest hue to hold.",
    "Tyger Tyger, burning bright, In the forests of the night.",
    "Do not stand at my grave and weep; I am not there. I do not sleep.",
    "I met a traveller from an antique land Who said: Two vast and trunkless legs of stone Stand in the desert.",
    "There is another sky, Ever serene and fair, And there is another sunshine.",
    "Two roads diverged in a wood, and I— I took the one less traveled by, And that has made all the difference."
]

# ======================================
# Analyseur lexical
# ======================================

tokens = ['WORD', 'COMMA', 'DOT', 'QUESTION', 'EXCLAMATION', 'NEWLINE','QUOTE']
t_COMMA = r','
t_DOT = r'\.'
t_QUESTION = r'\?'
t_EXCLAMATION = r'!'
t_QUOTE = r"[’']"
t_ignore = ' \t'

def t_WORD(t):
    r"[a-zA-ZÀ-ÿ\u0621-\u064A\u0600-\u06FF'-]+"
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_error(t):
    st.error(f"Caractère illégal ignoré : '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def analyze_lexical(input_text, poems):
    """Analyse lexicale avec correspondances."""
    lexer.input(input_text)
    tokens = [token.value for token in lexer]

    # Vérifications dans les poèmes
    full_matches = []
    partial_matches = []
    word_matches = {}

    for i, poem in enumerate(poems):
        if input_text.strip() == poem.strip():
            full_matches.append(poem)
        elif input_text.strip() in poem:
            partial_matches.append(poem)
        for word in tokens:
            if word in poem:
                if word not in word_matches:
                    word_matches[word] = []
                word_matches[word].append(poem)

    return tokens, full_matches, partial_matches, word_matches

# ======================================
# Analyse syntaxique et sémantique
# ======================================



# Règles syntaxiques pour les poèmes
def p_poem(p):
    '''poem : line
            | line NEWLINE poem'''
    pass

def p_line(p):
    '''line : WORD
            | WORD COMMA line
            | WORD DOT
            | WORD EXCLAMATION
            | WORD QUESTION
            | WORD QUOTE line
            | QUOTE line QUOTE
            | line WORD'''
    pass


def p_error(p):
    """
    Gestion des erreurs syntaxiques.
    """
    if p:
        raise Exception(f"Erreur syntaxique au token : {p.value}")
    else:
        raise Exception("Erreur syntaxique : fin de fichier inattendue.")
import re

def analyze_semantics(input_text):
    """
    Analyse sémantique d'un poème pour détecter des anomalies.
    """
    observations = []

    # Vérification de la longueur minimale
    if len(input_text.split()) < 3:
        observations.append("Le texte semble trop court pour être un poème.")

    # Vérification des majuscules
    if input_text == input_text.upper():
        observations.append("Le texte est entièrement en majuscules, ce qui peut être incohérent pour un poème.")


    # Vérification des virgules consécutives
    if re.search(r',,{1,}', input_text):
        observations.append("Le texte contient des virgules consécutives, ce qui est incorrect.")

    # Vérification des points consécutifs
    if re.search(r'\.{2,}', input_text):
        observations.append("Le texte contient des points consécutifs, ce qui est incorrect.")

    # Vérification des points d'exclamation consécutifs
    if re.search(r'!{2,}', input_text):
        observations.append("Le texte contient des points d'exclamation consécutifs, ce qui est incorrect.")

    # Vérification des points d'interrogation consécutifs
    if re.search(r'\?{2,}', input_text):
        observations.append("Le texte contient des points d'interrogation consécutifs, ce qui est incorrect.")



    # Vérification des lignes vides
    lines = input_text.split('\n')
    for i, line in enumerate(lines):
        if len(line.strip()) == 0 and i != len(lines) - 1:  # Ignorer la dernière ligne vide
            observations.append("Une ou plusieurs lignes sont vides, ce qui peut indiquer une incohérence.")

    # Vérification des lignes sans mots
    for line in lines:
        words = [word for word in line.split() if word.isalpha()]
        if len(words) == 0 and len(line.strip()) > 0:
            observations.append(f"La ligne suivante ne contient aucun mot : \"{line.strip()}\"")

    return observations


def analyze_syntax(input_text):
    """
    Analyse syntaxique d'un texte d'entrée pour vérifier s'il respecte les règles définies pour les poèmes.
    """
    try:
        # Crée le parser à partir des règles définies
        parser = yacc.yacc()

        # Effectue l'analyse syntaxique sur le texte d'entrée
        parser.parse(input_text)

        # Si aucune erreur détectée
        return "Aucune erreur syntaxique détectée."
    except Exception as e:
        # Retourne un message d'erreur clair
        return f"Erreur syntaxique : {e}"




# ======================================
# Traduction
# ======================================

def translate_line(line, source_lang, target_lang):
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        return translator.translate(line)
    except Exception as e:
        return f"Erreur de traduction: {e}"

def translate_poem(poem_lines, source_lang, target_lang):
    return [translate_line(line, source_lang, target_lang) for line in poem_lines]


# ======================================
# Reconnaissance vocale et analyse
# ======================================

def transcribe_audio():
    """
    Reconnaît un poème récité via le microphone et le transcrit.
    :return: Texte transcrit ou message d'erreur.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("Veuillez réciter votre poème...")
            recognizer.adjust_for_ambient_noise(source)  # Ajuste pour le bruit ambiant
            audio = recognizer.listen(source)
            st.info("Transcription en cours...")
            transcription = recognizer.recognize_google(audio, language="fr-FR")
            return transcription
    except sr.UnknownValueError:
        return "Erreur : Impossible de comprendre l'audio."
    except sr.RequestError as e:
        return f"Erreur de reconnaissance vocale : {e}"


def compare_transcription_with_poems(transcribed_text, known_poems):
    """
    Compare une transcription avec des poèmes connus pour trouver des correspondances.
    :param transcribed_text: Texte transcrit via reconnaissance vocale.
    :param known_poems: Liste des poèmes connus.
    :return: Liste de correspondances avec leurs scores.
    """
    matches = []
    for poem in known_poems:
        similarity = difflib.SequenceMatcher(None, transcribed_text, poem).ratio()
        if similarity > 0.6:  # Seuil de similarité
            matches.append((poem, similarity))
    matches.sort(key=lambda x: x[1], reverse=True)  # Trie par score décroissant
    return matches


# ======================================
# Application Streamlit
# ======================================

st.title("Poetry Translator and Verifier")
language = st.selectbox("Langue du poème :", ["Français", "Arabe", "Anglais"])
target_lang = st.selectbox("Traduire vers :", ["Français", "Arabe", "Anglais"])
poems = {"Français": french_poems, "Arabe": arabic_poems, "Anglais": english_poems}[language]
input_text = st.text_area("Écrivez ou collez votre texte ici :", height=200)

if st.button("Analyser et Vérifier"):
    if not input_text.strip():
        st.error("Veuillez entrer du texte avant de continuer.")
    else:
        st.subheader("Analyse Lexicale")
        tokens, full_matches, partial_matches, word_matches = analyze_lexical(input_text, poems)
        st.write(f"Tokens : {tokens}")

        if full_matches:
            st.success(f"Correspondance complète trouvée dans : {full_matches}")
        if partial_matches:
            st.info(f"Correspondance partielle trouvée dans : {partial_matches}")
        if word_matches:
            st.warning("Mots trouvés :")
            for word, occurrences in word_matches.items():
                st.write(f"**{word}** trouvé dans : {occurrences}")

        st.subheader("Analyse Syntaxique")
        syntax_result = analyze_syntax(input_text)
        st.write(syntax_result)

        st.subheader("Analyse Sémantique")
        semantic_results = analyze_semantics(input_text)
        if semantic_results:
            for obs in semantic_results:
                st.warning(obs)
        else:
            st.success("Aucune anomalie sémantique détectée.")

        st.subheader("Traduction")
        poem_lines = input_text.split('\n')
        translated_poem = translate_poem(poem_lines, language.lower()[:2], target_lang.lower()[:2])
        st.text_area("Poème traduit :", "\n".join(translated_poem), height=200)

# Ajout de la fonctionnalité de récitation vocale
st.subheader("Récitation Vocale")
if st.button("Réciter un poème"):
    # Transcrire l'audio
    transcribed_text = transcribe_audio()

    st.subheader("Texte Transcrit")
    if "Erreur" in transcribed_text:
        st.error(transcribed_text)
    else:
        st.success(transcribed_text)

        # Comparer avec les poèmes connus
        st.subheader("Comparaison avec des Poèmes Connus")
        matches = compare_transcription_with_poems(transcribed_text, poems)

        if matches:
            for poem, similarity in matches:
                st.info(f"Correspondance trouvée ({similarity * 100:.2f}% de similarité) :\n{poem}")
        else:
            st.warning("Aucune correspondance trouvée.")
