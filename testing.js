// Start from the root element
const rootElement = document.querySelector("#root > msn-windows-page > fluent-design-system-provider > div.root > div.content > grid-view-feed");

// Access the shadow root of the cs-super-container
const superContainerShadowRoot = rootElement.shadowRoot.querySelector("div > div.feed > cs-super-container").shadowRoot;

// Find the cs-personalized-feed shadow root
const personalizedFeedShadowRoot = superContainerShadowRoot.querySelector("cs-personalized-feed").shadowRoot;

// Locate the first cs-feed-layout shadow root (you can adjust the index as needed)
const feedLayoutShadowRoot = personalizedFeedShadowRoot.querySelector("cs-feed-layout:nth-child(1)").shadowRoot;

// Select all cs-native-ad-card elements and their parent containers
const adCards = feedLayoutShadowRoot.querySelectorAll("cs-native-ad-card");
adCards.forEach((adCard) => {
  const parentContainer = adCard.closest(".card-container");
  if (parentContainer) {
    // Hide or manipulate the parent container as needed
    parentContainer.style.display = "none";
  }
});
