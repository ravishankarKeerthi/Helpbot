// Helpbot - advanced conversational help widget
frappe.after_ajax(() => {
	if (window.location.pathname.includes("/login")) return;
	if (document.getElementById("helpbot-bubble")) return;

	const QUICK_CHIPS = [
		"How to create a Sales Invoice",
		"Leave approval process",
		"GST setup",
		"Stock reconciliation",
		"I'm getting an error",
	];

	// Floating bubble
	const bubble = document.createElement("div");
	bubble.id = "helpbot-bubble";
	bubble.innerHTML = `<span class="helpbot-bubble-icon">💬</span>`;
	bubble.title = "Ask Docbot";
	document.body.appendChild(bubble);

	// Chat panel
	const panel = document.createElement("div");
	panel.id = "helpbot-panel";
	panel.innerHTML = `
		<div id="helpbot-header">
			<div class="helpbot-avatar">SB</div>
			<div class="helpbot-header-text">
				<div class="helpbot-title">Helpbot</div>
				<div class="helpbot-subtitle">
					<span class="helpbot-status-dot"></span> Online · Internal + ERPNext docs
				</div>
			</div>
			<span id="helpbot-close">&times;</span>
		</div>
		<div id="helpbot-messages"></div>
		<div id="helpbot-inputbar">
			<input type="text" id="helpbot-input" placeholder="Type your question..." autocomplete="off" />
			<button id="helpbot-send" title="Send">&#10148;</button>
		</div>
	`;
	document.body.appendChild(panel);

	const messages = panel.querySelector("#helpbot-messages");
	const input = panel.querySelector("#helpbot-input");
	const sendBtn = panel.querySelector("#helpbot-send");

	function showWelcome() {
		messages.innerHTML = "";
		appendBotBubble(`
			<div>Hi 👋 Ask me anything about our internal workflows or ERPNext features.</div>
			<div class="helpbot-chips">
				${QUICK_CHIPS.map(
					(c) => `<span class="helpbot-chip" data-q="${frappe.utils.escape_html(c)}">${c}</span>`
				).join("")}
			</div>
		`);
		messages.querySelectorAll(".helpbot-chip").forEach((chip) => {
			chip.addEventListener("click", () => {
				input.value = chip.dataset.q;
				handleSend();
			});
		});
	}

	bubble.addEventListener("click", () => {
		const isOpen = panel.classList.toggle("helpbot-open");
		bubble.classList.toggle("helpbot-bubble-hidden", isOpen);
		if (isOpen && !messages.dataset.loaded) {
			showWelcome();
			messages.dataset.loaded = "1";
		}
		if (isOpen) setTimeout(() => input.focus(), 200);
	});

	panel.querySelector("#helpbot-close").addEventListener("click", () => {
		panel.classList.remove("helpbot-open");
		bubble.classList.remove("helpbot-bubble-hidden");
	});

	function appendUserBubble(text) {
		const div = document.createElement("div");
		div.className = "helpbot-msg helpbot-msg-user";
		div.innerHTML = `<div class="helpbot-bubble-text">${frappe.utils.escape_html(text)}</div>`;
		messages.appendChild(div);
		scrollToBottom();
	}

	function appendBotBubble(html) {
		const div = document.createElement("div");
		div.className = "helpbot-msg helpbot-msg-bot";
		div.innerHTML = `
			<div class="helpbot-avatar-sm">SB</div>
			<div class="helpbot-bubble-text">${html}</div>
		`;
		messages.appendChild(div);
		scrollToBottom();
		return div;
	}

	function showTyping() {
		const div = document.createElement("div");
		div.className = "helpbot-msg helpbot-msg-bot helpbot-typing";
		div.innerHTML = `
			<div class="helpbot-avatar-sm">SB</div>
			<div class="helpbot-bubble-text helpbot-typing-dots">
				<span></span><span></span><span></span>
			</div>
		`;
		messages.appendChild(div);
		scrollToBottom();
		return div;
	}

	function scrollToBottom() {
		messages.scrollTop = messages.scrollHeight;
	}

	function handleSend() {
		const query = input.value.trim();
		if (!query) return;
		appendUserBubble(query);
		input.value = "";
		const typingEl = showTyping();

		frappe.call({
			method: "helpbot.api.search_help",
			args: { query: query },
			callback: function (r) {
				typingEl.remove();
				renderResults(r.message || [], query);
			},
			error: function () {
				typingEl.remove();
				appendBotBubble(`<div>Something went wrong searching. Try again in a moment.</div>`);
			},
		});
	}

	function renderResults(matches, query) {
		if (!matches.length) {
			frappe.call({
				method: "helpbot.api.get_official_docs_search_url",
				args: { query: query },
				callback: function (r) {
					appendBotBubble(`
						<div>I couldn't find an internal article for that.</div>
						<a class="helpbot-external-link" href="${r.message}" target="_blank">
							🔗 Search ERPNext official docs for "${frappe.utils.escape_html(query)}"
						</a>
					`);
				},
			});
			return;
		}

		const cardsHtml = matches
			.map((m) => {
				const badge = m.category === "Error Resolution"
					? `<span class="helpbot-badge error">Error Fix</span>`
					: m.is_official_erpnext_doc
						? `<span class="helpbot-badge official">Official Docs</span>`
						: `<span class="helpbot-badge internal">Internal</span>`;
				const link = m.reference_url
					? `<a href="${m.reference_url}" target="_blank" class="helpbot-card-link">Open reference &rarr;</a>`
					: "";
				const cleanContent = (m.content || "")
					.replace(/<\/p>|<br\s*\/?>/gi, " ")
					.replace(/<[^>]*>/g, "")
					.replace(/\s+/g, " ")
					.trim();
				const preview = cleanContent.slice(0, 160);
				const isTruncated = cleanContent.length > 160;
				const rootCause = m.root_cause
					? `<div class="helpbot-card-root-cause"><b>Likely cause:</b> ${frappe.utils.escape_html(m.root_cause)}</div>`
					: "";
				const cardId = "helpbot-card-" + Math.random().toString(36).slice(2, 9);

				return `
					<div class="helpbot-card">
						<div class="helpbot-card-title">${frappe.utils.escape_html(m.title)} ${badge}</div>
						${m.module ? `<div class="helpbot-card-module">${m.module}</div>` : ""}
						${rootCause}
						<div class="helpbot-card-preview" id="${cardId}-preview">${preview}${isTruncated ? "..." : ""}</div>
						<div class="helpbot-card-full" id="${cardId}-full" style="display:none;">${m.content || ""}</div>
						${isTruncated ? `<a href="#" class="helpbot-card-link helpbot-expand-link" data-target="${cardId}">Read full guide &rarr;</a>` : ""}
						${link}
					</div>
				`;
			})
			.join("");

		const bubbleEl = appendBotBubble(`<div class="helpbot-cards">${cardsHtml}</div>`);

		bubbleEl.querySelectorAll(".helpbot-expand-link").forEach((el) => {
			el.addEventListener("click", (e) => {
				e.preventDefault();
				const id = el.dataset.target;
				const previewEl = bubbleEl.querySelector(`#${id}-preview`);
				const fullEl = bubbleEl.querySelector(`#${id}-full`);
				const expanded = fullEl.style.display !== "none";
				fullEl.style.display = expanded ? "none" : "block";
				previewEl.style.display = expanded ? "block" : "none";
				el.textContent = expanded ? "Read full guide →" : "Show less ↑";
				scrollToBottom();
			});
		});
	}

	sendBtn.addEventListener("click", handleSend);
	input.addEventListener("keydown", (e) => {
		if (e.key === "Enter") handleSend();
	});
});
