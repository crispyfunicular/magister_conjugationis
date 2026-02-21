function conjugationApp() {
  return {
    screen: "setup",
    isLoading: true,
    loadError: "",
    verbs: [],
    tenses: [],
    groups: [],
    pool: [],
    personOptions: [
      { value: 1, label: "1e du singulier" },
      { value: 2, label: "2e du singulier" },
      { value: 3, label: "3e du singulier" },
      { value: 4, label: "1e du pluriel" },
      { value: 5, label: "2e du pluriel" },
      { value: 6, label: "3e du pluriel" },
    ],
    session: {
      count: 10,
      direction: "aleatoire",
      tenses: [],
      moods: [],
      voices: [],
      persons: [],
      groups: [],
    },
    quiz: {
      totalRounds: 0,
      roundIndex: 0,
      totalScore: 0,
      current: null,
      subScore: 0,
      pendingScore: null,
      showHintsModal: false,
      latinSelections: {
        person: "",
        tense: "",
        voice: "",
        mood: "",
        translation: "",
      },
      correctTranslation: "",
      inputAnswer: "",
      translationOptions: [],
      feedback: null,
      awaitingAction: false,
      showPrimitives: false,
      showLemma: false,
      revealed: false,
    },
    init() {
      this.loadVerbs();
    },
    async loadVerbs() {
      this.isLoading = true;
      this.loadError = "";
      try {
        // Prefer embedded dataset to avoid CORS issues on static hosting.
        if (window.VERBS_LATIN && Array.isArray(window.VERBS_LATIN)) {
          this.verbs = window.VERBS_LATIN;
        } else {
          const response = await fetch("verbs_latin.json");
          if (!response.ok) {
            throw new Error("Impossible de charger verbs_latin.json");
          }
          this.verbs = await response.json();
        }
        this.tenses = this.buildTenses();
        this.groups = this.buildGroups();
        this.pool = this.verbs;
      } catch (error) {
        this.loadError =
          "Impossible de charger les verbes. Vérifiez verbs_latin.js ou les permissions du navigateur.";
      } finally {
        this.isLoading = false;
      }
    },
    buildTenses() {
      const order = [
        "présent",
        "imparfait",
        "futur",
        "parfait",
        "plus-que-parfait",
        "futur antérieur",
      ];
      const set = new Set(this.verbs.map((verb) => verb.tense));
      const sorted = [];
      order.forEach((tense) => {
        if (set.has(tense)) {
          set.delete(tense);
          sorted.push(tense);
        }
      });
      return [...sorted, ...Array.from(set).sort((a, b) => a.localeCompare(b))];
    },
    buildGroups() {
      const set = new Set(this.verbs.map((verb) => verb.group));
      return Array.from(set).sort((a, b) => a - b);
    },
    formatPerson(person) {
      if (!person) {
        return "";
      }
      const isPlural = Number(person) > 3;
      const value = isPlural ? Number(person) - 3 : Number(person);
      const suffix = isPlural ? "pluriel" : "singulier";
      return `${value}e du ${suffix}`;
    },
    filteredVerbs() {
      const hasTenses = this.session.tenses.length > 0;
      const hasMoods = this.session.moods.length > 0;
      const hasVoices = this.session.voices.length > 0;
      const hasPersons = this.session.persons.length > 0;
      const hasGroups = this.session.groups.length > 0;
      const personSet = new Set(this.session.persons.map(Number));
      const groupSet = new Set(this.session.groups.map(Number));
      const tenseSet = new Set(this.session.tenses);
      const moodSet = new Set(this.session.moods);
      const voiceSet = new Set(this.session.voices);

      return this.verbs.filter((verb) => {
        if (hasTenses && !tenseSet.has(verb.tense)) {
          return false;
        }
        if (hasMoods && !moodSet.has(verb.mood)) {
          return false;
        }
        if (hasVoices && !voiceSet.has(verb.voice)) {
          return false;
        }
        if (hasPersons && !personSet.has(verb.person)) {
          return false;
        }
        if (hasGroups && !groupSet.has(verb.group)) {
          return false;
        }
        return true;
      });
    },
    get filteredPool() {
      return this.filteredVerbs();
    },
    get filteredCount() {
      return this.filteredPool.length;
    },
    get totalCount() {
      return this.verbs.length;
    },
    startSession() {
      if (this.isLoading) {
        return;
      }
      this.pool = this.filteredVerbs();
      if (this.pool.length === 0) {
        this.loadError =
          "Aucun verbe ne correspond a ces filtres. Ajustez la selection.";
        return;
      }
      this.loadError = "";
      const count = Math.min(Math.max(this.session.count, 0), 100);
      if (count === 0) {
        this.quiz.totalRounds = 0;
        this.quiz.roundIndex = 0;
        this.quiz.totalScore = 0;
        this.screen = "summary";
        return;
      }
      this.quiz.totalRounds = count;
      this.quiz.roundIndex = 0;
      this.quiz.totalScore = 0;
      this.screen = "quiz";
      this.nextQuestion();
    },
    nextQuestion() {
      if (this.quiz.roundIndex >= this.quiz.totalRounds) {
        this.screen = "summary";
        return;
      }
      // Randomly select a verb and direction for the next round.
      const verb = this.pool[Math.floor(Math.random() * this.pool.length)];
      const direction =
        this.session.direction === "aleatoire"
          ? Math.random() > 0.5
            ? "latin"
            : "français"
          : this.session.direction;
      this.quiz.current = { verb, direction };
      this.quiz.subScore = 0;
      this.quiz.pendingScore = null;
      this.quiz.showHintsModal = false;
      this.quiz.latinSelections = {
        person: "",
        tense: "",
        voice: "",
        mood: "",
        translation: "",
      };
      this.quiz.inputAnswer = "";
      this.quiz.feedback = null;
      this.quiz.awaitingAction = false;
      this.quiz.showPrimitives = false;
      this.quiz.showLemma = false;
      this.quiz.revealed = false;
      // Only one correct translation is chosen per question.
      this.quiz.correctTranslation = this.pickCorrectTranslation(verb);
      this.quiz.translationOptions = this.buildTranslationOptions(
        verb,
        this.quiz.correctTranslation
      );
      this.applyLatinAutoSelections();
    },
    applyLatinAutoSelections() {
      const selections = this.quiz.latinSelections;

      if (this.allowedPersons.length === 1) {
        selections.person = this.allowedPersons[0];
      } else if (
        selections.person &&
        !this.allowedPersons.includes(String(selections.person))
      ) {
        selections.person = "";
      }

      if (this.allowedTenses.length === 1) {
        selections.tense = this.allowedTenses[0];
      } else if (selections.tense && !this.allowedTenses.includes(selections.tense)) {
        selections.tense = "";
      }

      if (this.allowedVoices.length === 1) {
        selections.voice = this.allowedVoices[0];
      } else if (selections.voice && !this.allowedVoices.includes(selections.voice)) {
        selections.voice = "";
      }

      if (this.allowedMoods.length === 1) {
        selections.mood = this.allowedMoods[0];
      } else if (selections.mood && !this.allowedMoods.includes(selections.mood)) {
        selections.mood = "";
      }
    },
    buildTranslationOptions(verb, correctTranslation) {
      // Exclude other translations of the same verb to avoid multiple valid choices.
      const options = new Set([correctTranslation]);
      const excluded = new Set(verb.translation || []);
      const targetCount = Math.max(6, options.size + 2);
      let guard = 0;
      while (options.size < targetCount && guard < 200) {
        const pick = this.verbs[Math.floor(Math.random() * this.verbs.length)];
        const translation =
          pick.translation[Math.floor(Math.random() * pick.translation.length)];
        if (!excluded.has(translation)) {
          options.add(translation);
        }
        guard += 1;
      }
      return this.shuffleArray(
        Array.from(options).map((value) => ({ value, label: value }))
      );
    },
    pickCorrectTranslation(verb) {
      if (!verb.translation || verb.translation.length === 0) {
        return "";
      }
      const index = Math.floor(Math.random() * verb.translation.length);
      return verb.translation[index];
    },
    shuffleArray(items) {
      const copy = [...items];
      for (let i = copy.length - 1; i > 0; i -= 1) {
        const j = Math.floor(Math.random() * (i + 1));
        [copy[i], copy[j]] = [copy[j], copy[i]];
      }
      return copy;
    },
    get quizDirectionLabel() {
      if (!this.quiz.current) {
        return "";
      }
      return this.quiz.current.direction === "latin"
        ? "Latin → français"
        : "Français → latin";
    },
    get allowedPersons() {
      const base = this.session.persons.length
        ? this.session.persons
        : this.personOptions.map((person) => person.value);
      return base.map((value) => String(value));
    },
    get personColumns() {
      const left = [1, 2, 3];
      const right = [4, 5, 6];
      return { left, right };
    },
    get allowedTenses() {
      return this.session.tenses.length ? this.session.tenses : this.tenses;
    },
    get tenseColumns() {
      return {
        left: ["présent", "imparfait", "futur"],
        right: ["parfait", "plus-que-parfait", "futur antérieur"],
      };
    },
    get allowedVoices() {
      return this.session.voices.length
        ? this.session.voices
        : ["actif", "passif", "déponent"];
    },
    get allowedMoods() {
      return this.session.moods.length
        ? this.session.moods
        : ["indicatif", "subjonctif"];
    },
    isPersonDisabled(value) {
      return !this.allowedPersons.includes(String(value));
    },
    isTenseDisabled(tense) {
      if (!this.tenses.includes(tense)) {
        return true;
      }
      return !this.allowedTenses.includes(tense);
    },
    get latinAnswersComplete() {
      const { person, tense, voice, mood, translation } =
        this.quiz.latinSelections;
      return Boolean(person && tense && voice && mood && translation);
    },
    get latinCorrectAnswers() {
      if (!this.quiz.current) {
        return {
          person: "",
          tense: "",
          voice: "",
          mood: "",
          translation: "",
        };
      }
      const verb = this.quiz.current.verb;
      return {
        person: this.formatPerson(verb.person),
        tense: verb.tense,
        voice: verb.voice,
        mood: verb.mood,
        translation: this.quiz.correctTranslation || verb.translation.join(", "),
      };
    },
    get directionLabel() {
      if (this.session.direction === "latin") {
        return "latin → français";
      }
      if (this.session.direction === "français") {
        return "français → latin";
      }
      return "aléatoire";
    },
    get selectedTensesLabel() {
      if (this.session.tenses.length === 0) {
        return "tous";
      }
      return this.session.tenses.join(", ");
    },
    get selectedMoodsLabel() {
      if (this.session.moods.length === 0) {
        return "tous";
      }
      return this.session.moods.join(", ");
    },
    get selectedVoicesLabel() {
      if (this.session.voices.length === 0) {
        return "toutes";
      }
      return this.session.voices.join(", ");
    },
    get selectedPersonsLabel() {
      if (this.session.persons.length === 0) {
        return "toutes";
      }
      const ordered = [...this.session.persons]
        .map(Number)
        .sort((a, b) => a - b)
        .map((person) => this.formatPerson(person));
      return ordered.join(", ");
    },
    get selectedGroupsLabel() {
      if (this.session.groups.length === 0) {
        return "tous";
      }
      const ordered = [...this.session.groups]
        .map(Number)
        .sort((a, b) => a - b)
        .join(", ");
      return ordered;
    },
    get scoreLabel() {
      return `${this.quiz.totalScore}/${this.quiz.totalRounds}`;
    },
    get quizPrompt() {
      if (!this.quiz.current) {
        return "";
      }
      const verb = this.quiz.current.verb;
      const translation = verb.translation.join(", ");
      return `Indiquer la forme fléchie pour ${translation}, ${this.formatPerson(
        verb.person
      )}, ${verb.tense}, ${verb.voice}, ${verb.mood} :`;
    },
    normalizeLatin(value) {
      return value
        .toLowerCase()
        .replaceAll("v", "u")
        .replaceAll("j", "i")
        .trim();
    },
    submitLatinBundle() {
      if (!this.latinAnswersComplete) {
        this.quiz.feedback = {
          type: "error",
          message: "Sélectionnez toutes les réponses.",
        };
        return;
      }
      const verb = this.quiz.current.verb;
      const correctCount =
        (Number(this.quiz.latinSelections.person) === verb.person ? 1 : 0) +
        (this.quiz.latinSelections.tense === verb.tense ? 1 : 0) +
        (this.quiz.latinSelections.voice === verb.voice ? 1 : 0) +
        (this.quiz.latinSelections.mood === verb.mood ? 1 : 0) +
        (this.quiz.latinSelections.translation ===
          this.quiz.correctTranslation
          ? 1
          : 0);

      if (correctCount === 5) {
        this.quiz.subScore = 1;
        this.quiz.feedback = { type: "success", message: "Bravo !" };
        this.quiz.awaitingAction = false;
        this.quiz.showPrimitives = false;
        this.quiz.revealed = false;
        setTimeout(() => {
          this.completeRound();
        }, 400);
      } else {
        this.quiz.feedback = { type: "error", message: "Mauvaise réponse !" };
        this.quiz.awaitingAction = true;
        this.quiz.showHintsModal = true;
      }
    },
    retryLatinBundle() {
      this.quiz.feedback = null;
      this.quiz.awaitingAction = false;
      this.quiz.showPrimitives = false;
      this.quiz.revealed = false;
      this.quiz.showHintsModal = false;
    },
    showPrimitives() {
      this.quiz.showPrimitives = true;
      this.quiz.showHintsModal = true;
    },
    showLemma() {
      this.quiz.showLemma = true;
      this.quiz.showHintsModal = true;
    },
    revealLatinBundle() {
      this.quiz.pendingScore = 0;
      this.quiz.revealed = true;
      this.quiz.awaitingAction = false;
      this.quiz.showHintsModal = true;
    },
    advanceAfterReveal() {
      if (this.quiz.pendingScore !== null) {
        this.quiz.subScore = this.quiz.pendingScore;
        this.quiz.pendingScore = null;
        this.quiz.showHintsModal = false;
        this.completeRound();
        return;
      }
      this.quiz.revealed = false;
      this.quiz.showPrimitives = false;
      this.quiz.showLemma = false;
      this.quiz.showHintsModal = false;
      this.completeRound();
    },
    submitLatinAnswer() {
      if (!this.quiz.inputAnswer) {
        this.quiz.feedback = {
          type: "error",
          message: "Indiquez une réponse.",
        };
        return;
      }
      const correct = this.quiz.current.verb.latin;
      if (
        this.normalizeLatin(this.quiz.inputAnswer) ===
        this.normalizeLatin(correct)
      ) {
        this.quiz.subScore = 1;
        this.quiz.feedback = { type: "success", message: "Bravo !" };
        this.quiz.awaitingAction = false;
        setTimeout(() => {
          this.completeRound();
        }, 400);
      } else {
        this.quiz.feedback = { type: "error", message: "Mauvaise réponse !" };
        this.quiz.awaitingAction = true;
        this.quiz.showHintsModal = true;
      }
    },
    retryLatinAnswer() {
      this.quiz.feedback = null;
      this.quiz.awaitingAction = false;
      this.quiz.showPrimitives = false;
      this.quiz.showLemma = false;
      this.quiz.revealed = false;
      this.quiz.showHintsModal = false;
    },
    revealLatinAnswer() {
      this.quiz.pendingScore = 0;
      this.quiz.revealed = true;
      this.quiz.awaitingAction = false;
      this.quiz.showHintsModal = true;
    },
    completeRound() {
      this.quiz.totalScore += this.quiz.subScore;
      this.quiz.roundIndex += 1;
      this.nextQuestion();
    },
    resetSession() {
      this.quiz = {
        totalRounds: 0,
        roundIndex: 0,
        totalScore: 0,
        current: null,
        subScore: 0,
        pendingScore: null,
        showHintsModal: false,
        correctTranslation: "",
        latinSelections: {
          person: "",
          tense: "",
          voice: "",
          mood: "",
          translation: "",
        },
        inputAnswer: "",
        translationOptions: [],
        feedback: null,
        awaitingAction: false,
        showPrimitives: false,
        showLemma: false,
        revealed: false,
      };
      this.screen = "setup";
    },
  };
}
