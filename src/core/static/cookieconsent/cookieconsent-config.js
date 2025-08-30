import "https://cdn.jsdelivr.net/gh/orestbida/cookieconsent@3.1.0/dist/cookieconsent.umd.js";

// Enable dark mode
document.documentElement.classList.add("cc--light-funky");

CookieConsent.run({
  guiOptions: {
    consentModal: {
      layout: "box",
      position: "bottom right",
      equalWeightButtons: true,
      flipButtons: false,
    },
    preferencesModal: {
      layout: "box",
      position: "right",
      equalWeightButtons: true,
      flipButtons: false,
    },
  },
  categories: {
    necessary: {
      readOnly: true,
    },
    analytics: {},
  },
  language: {
    default: "pl",
    autoDetect: "browser",
    translations: {
      pl: {
        consentModal: {
          title: "Szanujemy prywatność naszych użytkowników.",
          description:
            "Wykorzystujemy pliki cookie, aby ulepszyć doświadczenie przeglądania, prezentować spersonalizowane reklamy lub treści oraz monitorować ruch na stronie. Kliknięcie „Akceptuj wszystkie” wyraża zgodę na używanie przez nas plików cookie.",
          acceptAllBtn: "Akceptuj wszystkie",
          acceptNecessaryBtn: "Odrzuć wszystkie",
          showPreferencesBtn: "",
          footer: '<a href="/polityka-prywatnosci/">Polityka prywatności</a>',
        },
      },
    },
  },
});
