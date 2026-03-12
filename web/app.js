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
      history: [],
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
      hasErred: false,
      latinErrors: { person: false, tense: false, voice: false, mood: false, translation: false },
      validProfiles: [],
      acceptedLatins: [],
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
      this.quiz.history = [];
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
      this.quiz.hasErred = false;
      this.quiz.latinErrors = { person: false, tense: false, voice: false, mood: false, translation: false };
      // Syncrétisme : calculer les profils valides (Latin→FR) et formes acceptées (FR→Latin)
      this.quiz.validProfiles = this.verbs.filter((v) => v.latin === verb.latin);
      this.quiz.acceptedLatins = [...new Set(
        this.pool
          .filter(
            (v) =>
              v.person === verb.person &&
              v.tense === verb.tense &&
              v.voice === verb.voice &&
              v.mood === verb.mood &&
              v.translation.some((t) => verb.translation.includes(t))
          )
          .map((v) => v.latin)
      )];
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

      this.onMoodChange();
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
    isVoiceDisabled(voice) {
      if (!this.allowedVoices.includes(voice)) return true;
      return false;
    },
    get allowedMoods() {
      return this.session.moods.length
        ? this.session.moods
        : ["indicatif", "subjonctif", "impératif"];
    },
    get isImperativeOnly() {
      return this.session.moods.length === 1 && this.session.moods[0] === 'impératif';
    },
    get isSubjunctiveOnly() {
      return this.session.moods.length === 1 && this.session.moods[0] === 'subjonctif';
    },
    // Subjunctive only exists for présent, imparfait, parfait, plus-que-parfait
    get subjunctiveTenses() {
      return ['présent', 'imparfait', 'parfait', 'plus-que-parfait'];
    },
    get isSubjunctiveDisabled() {
      const { tenses } = this.session;
      // If tenses are selected but none is compatible with subjunctive → no subjunctive possible
      const disabled = tenses.length > 0 && !tenses.some(t => this.subjunctiveTenses.includes(t));
      if (disabled && this.session.moods.includes('subjonctif')) {
        this.session.moods = this.session.moods.filter(m => m !== 'subjonctif');
      }
      return disabled;
    },
    get isImperativeDisabled() {
      const { tenses, persons, groups } = this.session;
      // If tenses are selected but none is présent → no imperative possible
      const disabled = (tenses.length > 0 && !tenses.includes('présent'))
        // If persons are selected and none is 2 or 5 → no imperative possible
        || (persons.length > 0 && !persons.some(p => Number(p) === 2 || Number(p) === 5))
        // If only group 0 is selected → no imperative possible (sum/esse)
        || (groups.length > 0 && groups.every(g => Number(g) === 0));
      if (disabled && this.session.moods.includes('impératif')) {
        this.session.moods = this.session.moods.filter(m => m !== 'impératif');
      }
      return disabled;
    },
    get isPassiveDeponentDisabled() {
      const { groups } = this.session;
      // GP0 (sum, esse) only has active voice — no passive or deponent
      const disabled = groups.length > 0 && groups.every(g => Number(g) === 0);
      if (disabled) {
        const blocked = ['passif', 'déponent'];
        if (this.session.voices.some(v => blocked.includes(v))) {
          this.session.voices = this.session.voices.filter(v => !blocked.includes(v));
        }
      }
      return disabled;
    },
    get isGroup0Disabled() {
      const { voices, moods } = this.session;
      // GP0 (sum/esse) has no passive, deponent, or imperative forms
      const disabled = (voices.length > 0 && voices.every(v => v === 'passif' || v === 'déponent'))
        || (moods.length > 0 && moods.every(m => m === 'impératif'));
      if (disabled && this.session.groups.some(g => Number(g) === 0)) {
        this.session.groups = this.session.groups.filter(g => Number(g) !== 0);
      }
      return disabled;
    },
    isTenseDisabledSetup(tense) {
      const disabled = (this.isImperativeOnly && tense !== 'présent')
        || (this.isSubjunctiveOnly && !this.subjunctiveTenses.includes(tense));
      if (disabled && this.session.tenses.includes(tense)) {
        this.session.tenses = this.session.tenses.filter(t => t !== tense);
      }
      return disabled;
    },
    isPersonDisabled(value) {
      if (!this.allowedPersons.includes(String(value))) return true;
      // Imperative only exists for 2nd person singular (2) and plural (5).
      // Only apply this restriction if at least one imperative-compatible
      // person is available, to avoid a deadlock where no person can be selected.
      if (this.quiz.latinSelections.mood === 'impératif' && value !== 2 && value !== 5) {
        const hasImperativePerson = this.allowedPersons.includes('2') || this.allowedPersons.includes('5');
        if (hasImperativePerson) return true;
      }
      return false;
    },
    isMoodDisabledQuiz(mood) {
      if (!this.allowedMoods.includes(mood)) return true;
      // Imperative only exists for persons 2 and 5
      if (mood === 'impératif') {
        const hasImperativePerson = this.allowedPersons.includes('2') || this.allowedPersons.includes('5');
        if (!hasImperativePerson) return true;
      }
      return false;
    },
    isTenseDisabled(tense) {
      if (!this.tenses.includes(tense)) return true;
      if (!this.allowedTenses.includes(tense)) return true;
      // Imperative only exists in the present tense
      if (this.quiz.latinSelections.mood === 'impératif' && tense !== 'présent') return true;
      return false;
    },
    onMoodChange() {
      const sel = this.quiz.latinSelections;
      if (sel.mood === 'impératif') {
        sel.tense = 'présent';
        // Clear person if not compatible with imperative, but only if
        // there is at least one imperative-compatible person available.
        const hasImperativePerson = this.allowedPersons.includes('2') || this.allowedPersons.includes('5');
        if (hasImperativePerson && sel.person && sel.person !== '2' && sel.person !== '5') sel.person = '';
      }
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
          latin: "",
        };
      }
      const profiles = this.quiz.validProfiles;
      const unique = (arr) => [...new Set(arr)];
      // Pour Latin→FR : montrer toutes les analyses valides des profils restants
      const persons = unique(profiles.map((p) => this.formatPerson(p.person)));
      const tenses = unique(profiles.map((p) => p.tense));
      const voices = unique(profiles.map((p) => p.voice));
      const moods = unique(profiles.map((p) => p.mood));
      const translations = unique(profiles.flatMap((p) => p.translation));
      return {
        person: persons.join(" / "),
        tense: tenses.join(" / "),
        voice: voices.join(" / "),
        mood: moods.join(" / "),
        translation: translations.join(", "),
        latin: this.quiz.acceptedLatins.join(", "),
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
      // Logique de l'entonnoir : vérifier chaque réponse contre les profils valides restants
      const profiles = this.quiz.validProfiles;
      const sel = this.quiz.latinSelections;
      const personOk = profiles.some((p) => p.person === Number(sel.person));
      const tenseOk = profiles.some((p) => p.tense === sel.tense);
      const voiceOk = profiles.some((p) => p.voice === sel.voice);
      const moodOk = profiles.some((p) => p.mood === sel.mood);
      // Pour la traduction, collecter toutes les traductions des profils restants
      const allTranslations = new Set(profiles.flatMap((p) => p.translation));
      const translationOk = allTranslations.has(sel.translation);

      // Vérifier la cohérence globale : les réponses doivent correspondre à AU MOINS un profil complet
      const coherent = profiles.some(
        (p) =>
          p.person === Number(sel.person) &&
          p.tense === sel.tense &&
          p.voice === sel.voice &&
          p.mood === sel.mood &&
          p.translation.includes(sel.translation)
      );

      if (coherent) {
        // Resserrer l'entonnoir pour le reveal
        this.quiz.validProfiles = profiles.filter(
          (p) =>
            p.person === Number(sel.person) &&
            p.tense === sel.tense &&
            p.voice === sel.voice &&
            p.mood === sel.mood
        );
        this.quiz.subScore = this.quiz.hasErred ? 0.5 : 1;
        this.quiz.feedback = { type: "success", message: "Bravo !" };
        this.quiz.awaitingAction = false;
        this.quiz.showPrimitives = false;
        this.quiz.revealed = false;
        setTimeout(() => {
          this.completeRound();
        }, 400);
      } else {
        // Indiquer les erreurs par champ
        this.quiz.latinErrors = {
          person: !personOk,
          tense: !tenseOk,
          voice: !voiceOk,
          mood: !moodOk,
          translation: !translationOk,
        };
        this.quiz.hasErred = true;
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
      // Syncrétisme : vérifier contre toutes les formes latines acceptées
      const normalizedInput = this.normalizeLatin(this.quiz.inputAnswer);
      const isCorrect = this.quiz.acceptedLatins.some(
        (lat) => normalizedInput === this.normalizeLatin(lat)
      );
      if (isCorrect) {
        this.quiz.subScore = this.quiz.hasErred ? 0.5 : 1;
        this.quiz.feedback = { type: "success", message: "Bravo !" };
        this.quiz.awaitingAction = false;
        setTimeout(() => {
          this.completeRound();
        }, 400);
      } else {
        this.quiz.hasErred = true;
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
    skipQuestion() {
      this.quiz.subScore = 0;
      this.completeRound();
    },
    completeRound() {
      this.quiz.totalScore += this.quiz.subScore;
      if (this.quiz.current) {
        const verb = this.quiz.current.verb;
        this.quiz.history.push({
          latin: this.quiz.acceptedLatins.join(', '),
          person: this.formatPerson(verb.person),
          tense: verb.tense,
          voice: verb.voice,
          mood: verb.mood,
          translation: verb.translation.join(', '),
          score: this.quiz.subScore,
        });
      }
      this.quiz.roundIndex += 1;
      this.nextQuestion();
    },
    resetSession() {
      this.quiz = {
        totalRounds: 0,
        roundIndex: 0,
        totalScore: 0,
        history: [],
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
        hasErred: false,
        latinErrors: { person: false, tense: false, voice: false, mood: false, translation: false },
        validProfiles: [],
        acceptedLatins: [],
      };
      this.screen = "setup";
    },
    resetFilters() {
      this.session = {
        count: 10,
        direction: "aleatoire",
        tenses: [],
        moods: [],
        voices: [],
        persons: [],
        groups: [],
      };
    },
  };
}
