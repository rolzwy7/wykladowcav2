// Czekamy na pełne załadowanie DOM, aby bezpiecznie manipulować elementami
document.addEventListener("DOMContentLoaded", function () {
  // --- Odniesienia do kontenerów w DOM ---
  const mainCatContainer = document.getElementById("megamenu-main-categories");
  const subCatContainer = document.getElementById("megamenu-sub-categories");
  const resultsContainer = document.getElementById("megamenu-results");

  /**
   * Funkcja do czyszczenia zawartości kontenera.
   * @param {HTMLElement} container - Element do wyczyszczenia.
   */
  function clearContainer(container) {
    if (container) container.innerHTML = "";
  }

  /**
   * Funkcja do wyświetlania wyników dla wybranej kategorii i podkategorii.
   * @param {string} mainCategory - Nazwa kategorii głównej.
   * @param {string} subCategory - Nazwa podkategorii (lub "Wszystko").
   */
  function showResults(mainCategory, subCategory) {
    clearContainer(resultsContainer);

    const activeSubCategory = subCatContainer.querySelector(
      `[data-subcategory="${subCategory}"]`
    );
    subCatContainer
      .querySelectorAll(".megamenu-item")
      .forEach((item) => item.classList.remove("active"));
    if (activeSubCategory) activeSubCategory.classList.add("active");

    const results = menuData[mainCategory]?.results[subCategory] || [];
    const resultsList = document.createElement("div");
    resultsList.className = "list-group list-group-flush";

    if (results.length > 0) {
      results.forEach((resultData) => {
        const resultItem = document.createElement("a");
        resultItem.href = resultData.url;
        resultItem.className =
          "list-group-item list-group-item-action border-0 p-3";
        if (resultData.url === "#") {
          resultItem.onclick = (e) => e.preventDefault();
        }

        const contentWrapper = document.createElement("div");
        contentWrapper.className = "d-flex align-items-start";

        const avatar = document.createElement("img");
        avatar.src = resultData.avatar;
        avatar.alt = resultData.title;
        avatar.className = "me-3 rounded";
        avatar.width = 64;
        avatar.height = 64;
        avatar.onerror = function () {
          this.src = "https://placehold.co/64x64/e2e8f0/475569?text=Img";
        };

        const textContent = document.createElement("div");
        textContent.className = "flex-grow-1";

        const title = document.createElement("h6");
        title.className = "mb-1 fw-bold";
        title.textContent = resultData.title;

        const lecturer_fullname = document.createElement("p");
        lecturer_fullname.className = "mb-1 text-muted small";
        lecturer_fullname.textContent = resultData.lecturer_fullname;

        const description = document.createElement("p");
        description.className = "mb-1 text-muted small";
        description.textContent = resultData.description;

        const metaInfo = document.createElement("div");
        metaInfo.className =
          "d-flex justify-content-between align-items-center mt-2";

        const dates = document.createElement("div");
        dates.className = "small text-secondary";

        if (resultData.dates && resultData.dates.length > 0) {
          dates.innerHTML = "";
          resultData.dates.forEach(function (date, idx) {
            const dateSpan = document.createElement("p");

            dateSpan.className = date.includes("DARMOWE")
              ? "mb-0 fw-bold text-primary"
              : "mb-0";

            dateSpan.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-calendar-event me-1" viewBox="0 0 16 16"><path d="M11 6.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5z"/><path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5M1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4z"/></svg> ${date}`;
            dates.appendChild(dateSpan);
          });
        }

        const price = document.createElement("div");
        price.className = "fw-bold";
        if (resultData.price != "None") {
          console.log(resultData.price);
          if (resultData.price == 9999) {
            price.textContent = "Za Darmo";
          } else {
            price.textContent =
              "od " + resultData.price + "zł " + priceAdnotation;
          }
        } else {
          price.textContent = "";
        }

        metaInfo.appendChild(dates);
        if (resultData.price) metaInfo.appendChild(price);

        textContent.appendChild(title);
        textContent.appendChild(lecturer_fullname);

        if (resultData.description) textContent.appendChild(description);
        textContent.appendChild(metaInfo);

        contentWrapper.appendChild(avatar);
        contentWrapper.appendChild(textContent);

        resultItem.appendChild(contentWrapper);
        resultsList.appendChild(resultItem);
      });
    } else {
      const noResultsItem = document.createElement("span");
      noResultsItem.className = "list-group-item border-0";
      noResultsItem.textContent = "Brak wyników do wyświetlenia.";
      resultsList.appendChild(noResultsItem);
    }
    resultsContainer.appendChild(resultsList);
  }

  /**
   * Funkcja do wyświetlania podkategorii dla wybranej kategorii głównej.
   * @param {string} categoryName - Nazwa wybranej kategorii głównej.
   */
  function showSubcategories(categoryName) {
    clearContainer(subCatContainer);
    clearContainer(resultsContainer);

    const activeMainCategory = mainCatContainer.querySelector(
      `[data-category="${categoryName}"]`
    );
    mainCatContainer
      .querySelectorAll(".megamenu-item")
      .forEach((item) => item.classList.remove("active"));
    if (activeMainCategory) activeMainCategory.classList.add("active");

    const subcategories = menuData[categoryName]?.subcategories || [];
    const subcategoriesList = document.createElement("div");
    subcategoriesList.className = "list-group";

    const allItem = document.createElement("a");
    allItem.href = "#";
    allItem.className = "list-group-item list-group-item-action megamenu-item";
    allItem.textContent = "Wszystko";
    allItem.dataset.subcategory = "Wszystko";
    allItem.onclick = (e) => {
      e.preventDefault();
      showResults(categoryName, "Wszystko");
    };
    subcategoriesList.appendChild(allItem);

    subcategories.forEach((subCatName) => {
      const subCatItem = document.createElement("a");
      subCatItem.href = "#";
      subCatItem.className =
        "list-group-item list-group-item-action megamenu-item";
      subCatItem.textContent = subCatName;
      subCatItem.dataset.subcategory = subCatName;
      subCatItem.onclick = (e) => {
        e.preventDefault();
        showResults(categoryName, subCatName);
      };
      subcategoriesList.appendChild(subCatItem);
    });

    subCatContainer.appendChild(subcategoriesList);
    showResults(categoryName, "Wszystko");
  }

  /**
   * Inicjalizacja menu - tworzenie listy kategorii głównych.
   */
  function initMenu() {
    clearContainer(mainCatContainer);
    const mainCategoriesList = document.createElement("div");
    mainCategoriesList.className = "list-group";

    const categories = Object.keys(menuData);
    categories.forEach((categoryName) => {
      const categoryValue = menuData[categoryName];
      const categoryItem = document.createElement("a");
      categoryItem.href = "#";
      categoryItem.className =
        "list-group-item list-group-item-action megamenu-item";
      categoryItem.innerHTML = `<span class="icon-shape icon-xs pe-1">${categoryValue.icon}</span> ${categoryName}`;
      categoryItem.dataset.category = categoryName;
      categoryItem.onclick = (e) => {
        e.preventDefault();
        showSubcategories(categoryName);
      };
      mainCategoriesList.appendChild(categoryItem);
    });
    mainCatContainer.appendChild(mainCategoriesList);

    if (categories.length > 0) {
      showSubcategories(categories[0]);
    }
  }

  // --- Uruchomienie menu ---
  initMenu();
});
