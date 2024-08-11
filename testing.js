// Ensure the script runs after the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
  // Start from the root element
  const rootElement = document.querySelector("#root > msn-windows-page > fluent-design-system-provider > div.root > div.content > grid-view-feed");

  if (!rootElement) return; // Safeguard against null selectors

  // Attempt to access the shadow root of the cs-super-container
  const superContainerShadowRoot = rootElement.shadowRoot && rootElement.shadowRoot.querySelector("div > div.feed > cs-super-container")?.shadowRoot;

  if (!superContainerShadowRoot) return; // Safeguard against null shadow roots

  // Find the cs-personalized-feed shadow root
  const personalizedFeedShadowRoot = superContainerShadowRoot.querySelector("cs-personalized-feed")?.shadowRoot;

  if (!personalizedFeedShadowRoot) return; // Safeguard against null shadow roots

  // Locate the first cs-feed-layout shadow root (you can adjust the index as needed)
  const feedLayoutShadowRoot = personalizedFeedShadowRoot.querySelector("cs-feed-layout:nth-child(1)")?.shadowRoot;

  if (!feedLayoutShadowRoot) return; // Safeguard against null shadow roots

  // Select all cs-native-ad-card elements and their parent containers
  const adCards = feedLayoutShadowRoot.querySelectorAll("cs-native-ad-card");

  adCards.forEach((adCard) => {
    const parentContainer = adCard.closest(".card-container");
    if (parentContainer) {
      // Hide or manipulate the parent container as needed
      parentContainer.style.display = "none";
    }
  });
});
