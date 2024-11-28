import streamlit as st
from deep_translator import GoogleTranslator
import ply.lex as lex
import ply.yacc as yacc
# Ceci est un commentaire pour tester


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

tokens = ['WORD', 'COMMA', 'DOT', 'QUESTION', 'EXCLAMATION', 'NEWLINE']
t_COMMA = r','
t_DOT = r'\.'
t_QUESTION = r'\?'
t_EXCLAMATION = r'!'
t_ignore = ' \t'

def t_WORD(t):
    r'[a-zA-Z\u0621-\u064A\u0600-\u06FF]+'
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

def analyze_syntax(input_text):
    try:
        parser = yacc.yacc()
        parser.parse(input_text)
        return "Aucune erreur syntaxique détectée."
    except Exception as e:
        return f"Erreur syntaxique : {e}"

def analyze_semantics(input_text):
    observations = []
    if len(input_text.split()) < 3:
        observations.append("Le texte semble trop court.")
    if input_text == input_text.upper():
        observations.append("Le texte est entièrement en majuscules, vérifiez la cohérence.")
    return observations

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
