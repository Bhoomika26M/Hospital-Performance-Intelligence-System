document.addEventListener("DOMContentLoaded", () => {
  const currentPage = document.body.dataset.page;
  document.querySelectorAll("[data-nav]").forEach((link) => {
    if (link.dataset.nav === currentPage) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    }
  });

  const menuButton = document.querySelector(".menu-toggle");
  const navigation = document.querySelector(".site-nav");
  if (menuButton && navigation) {
    menuButton.addEventListener("click", () => {
      const isOpen = navigation.classList.toggle("open");
      menuButton.setAttribute("aria-expanded", String(isOpen));
      menuButton.setAttribute("aria-label", isOpen ? "Close navigation" : "Open navigation");
    });
    navigation.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => {
      navigation.classList.remove("open");
      menuButton.setAttribute("aria-expanded", "false");
      menuButton.setAttribute("aria-label", "Open navigation");
    }));
  }

  document.querySelectorAll("[data-year]").forEach((node) => {
    node.textContent = new Date().getFullYear();
  });

  const revealItems = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries, activeObserver) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          activeObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  }

  // Optional Tableau embed: add an approved HTTPS Tableau URL to data-tableau-url.
  // Empty or invalid URLs leave the explanatory placeholder visible.
  document.querySelectorAll("[data-tableau-embed]").forEach((container) => {
    const rawUrl = container.dataset.tableauUrl;
    if (!rawUrl) return;
    try {
      const parsed = new URL(rawUrl);
      const validHost = parsed.hostname === "public.tableau.com" || parsed.hostname.endsWith(".tableau.com");
      if (parsed.protocol !== "https:" || !validHost) return;
      const frame = document.createElement("iframe");
      frame.src = parsed.href;
      frame.title = container.dataset.tableauTitle || "Embedded Tableau dashboard";
      frame.loading = "lazy";
      frame.referrerPolicy = "strict-origin-when-cross-origin";
      frame.allowFullscreen = true;
      frame.style.cssText = "display:block;width:100%;height:100%;min-height:0;max-width:100%;border:0;background:#fff";
      container.replaceChildren(frame);
    } catch (_) {
      // Keep the placeholder when the embed URL is invalid.
    }
  });

  // Fullscreen mode for each embedded Tableau dashboard.
  const fullscreenButtons = document.querySelectorAll("[data-fullscreen-toggle]");
  fullscreenButtons.forEach((button) => {
    button.addEventListener("click", async () => {
      const viewer = button.closest("[data-dashboard-viewer]");
      if (!viewer) return;

      try {
        if (document.fullscreenElement === viewer) {
          await document.exitFullscreen();
        } else if (!document.fullscreenElement && viewer.requestFullscreen) {
          await viewer.requestFullscreen();
        } else if (document.fullscreenElement) {
          await document.exitFullscreen();
          if (viewer.requestFullscreen) await viewer.requestFullscreen();
        } else {
          button.textContent = "Full screen unavailable";
          button.disabled = true;
        }
      } catch (_) {
        button.textContent = "Full screen unavailable";
        button.disabled = true;
      }
    });
  });

  document.addEventListener("fullscreenchange", () => {
    fullscreenButtons.forEach((button) => {
      const viewer = button.closest("[data-dashboard-viewer]");
      const isActive = Boolean(viewer && document.fullscreenElement === viewer);
      button.innerHTML = isActive
        ? '<span aria-hidden="true">⛶</span> Exit full screen'
        : '<span aria-hidden="true">⛶</span> Full screen';
      button.setAttribute("aria-label", isActive ? "Exit full screen" : "View dashboard full screen");
    });
  });

});
