// Hán Ngữ+ — Frontend App Logic
let currentLevel = 1;
let reviewWords = [];
let reviewIndex = 0;
let dialogueLevel = 0;

// Lesson state
let lessonWords = [];
let lessonIndex = 0;
let currentThemeId = null;

// Audio
function speak(text, rate = 0.85) {
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'zh-CN'; u.rate = rate; u.pitch = 1.0;
    window.speechSynthesis.speak(u);
}
function playReviewAudio(e) { e.stopPropagation(); const el = document.getElementById('fcChar'); if(el) speak(el.textContent); }
function playLessonAudio() { const el = document.getElementById('lsChar'); if(el) speak(el.textContent); }
function playDlgLine(id) { const el = document.getElementById('dlg-'+id); if(el) speak(el.textContent); }

// Navigation
function showPage(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById('page-' + page).classList.add('active');
    document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
    const link = document.querySelector(`.nav-links a[data-page="${page}"]`);
    if (link) link.classList.add('active');
    
    if (page === 'home') loadHome();
    if (page === 'review') loadReview();
    if (page === 'words') loadWords();
    if (page === 'dialogues') loadDialogues();
    if (page === 'progress') loadProgress();
}

// API
async function api(path, opts = {}) {
    try {
        const res = await fetch(path, {
            headers: { 'Content-Type': 'application/json' }, ...opts
        });
        return await res.json();
    } catch (e) { console.error('API:', e); return null; }
}

// === HOME: Clickable Theme Cards ===
async function loadHome() {
    const [stats, themes] = await Promise.all([
        api('/api/stats'),
        api('/api/themes')
    ]);
    if (stats) {
        document.getElementById('statDue').textContent = stats.due;
        document.getElementById('statLearned').textContent = stats.learned;
        document.getElementById('statTotal').textContent = stats.total;
        document.getElementById('statDlg').textContent = stats.dialogues || 0;
    }
    if (!themes || !themes.themes) return;
    
    const grid = document.getElementById('themeGrid');
    grid.innerHTML = '';
    
    themes.themes.forEach(t => {
        const pct = t.total_words > 0 ? Math.round((t.learned_words / t.total_words) * 100) : 0;
        const card = document.createElement('div');
        card.className = 'theme-card' + (pct >= 100 ? ' completed' : '');
        card.innerHTML = `
            <div class="theme-icon">${t.icon || '📖'}</div>
            <div class="theme-name">${t.name}</div>
            <div class="theme-desc">${t.description || ''}</div>
            <div class="theme-progress-bar"><div class="theme-progress-fill" style="width:${pct}%"></div></div>
            <div class="theme-badge">${t.learned_words}/${t.total_words}</div>
        `;
        card.onclick = () => openLesson(t.id, t.name);
        grid.appendChild(card);
    });
}

// === LESSON: Word-by-word ===
async function openLesson(themeId, themeName) {
    currentThemeId = themeId;
    const data = await api(`/api/themes/${themeId}`);
    if (!data || !data.words) return;
    
    lessonWords = data.words;
    lessonIndex = 0;
    
    document.getElementById('lessonTitle').textContent = themeName;
    document.getElementById('lessonContent').style.display = 'block';
    document.getElementById('lessonDone').style.display = 'none';
    showLessonWord();
    showPage('lesson');
}

function showLessonWord() {
    if (lessonIndex >= lessonWords.length) {
        document.getElementById('lessonContent').style.display = 'none';
        document.getElementById('lessonDone').style.display = 'block';
        document.getElementById('lessonSummary').textContent =
            `Bạn đã học ${lessonWords.length} từ trong chủ đề này.`;
        return;
    }
    
    const w = lessonWords[lessonIndex];
    document.getElementById('lsChar').textContent = w.simplified;
    document.getElementById('lsPinyin').textContent = w.pinyin;
    document.getElementById('lsMeaning').textContent = w.meanings[0];
    
    // Sino-Vietnamese
    const svEl = document.getElementById('lsSinoViet');
    if (w.sino_viet) {
        svEl.textContent = `Hán-Việt: ${w.sino_viet}`;
        svEl.style.display = 'block';
    } else { svEl.style.display = 'none'; }
    
    // Sentence
    const sentCn = document.getElementById('lsSentCn');
    const sentVi = document.getElementById('lsSentVi');
    if (w.sentence_cn) {
        sentCn.textContent = w.sentence_cn; sentCn.style.display = 'block';
        sentVi.textContent = w.sentence_vi; sentVi.style.display = 'block';
    } else { sentCn.style.display = 'none'; sentVi.style.display = 'none'; }
    
    // Context note
    const ctx = document.getElementById('lsContextNote');
    if (w.context_note) {
        ctx.textContent = '💡 ' + w.context_note;
        ctx.style.display = 'block';
    } else { ctx.style.display = 'none'; }
    
    document.getElementById('lessonProgress').textContent = `${lessonIndex + 1}/${lessonWords.length}`;
    
    // Dots
    const dots = document.getElementById('lsDots');
    dots.innerHTML = '';
    lessonWords.forEach((_, i) => {
        const dot = document.createElement('div');
        dot.className = 'lesson-dot' + (i === lessonIndex ? ' active' : '') + (i < lessonIndex ? ' done' : '');
        dots.appendChild(dot);
    });
    
    // Mark as learned
    if (!w.learned) {
        api(`/api/themes/${currentThemeId}/learn/${w.id}`, { method: 'POST' });
        w.learned = true;
    }
    
    // Nav buttons
    document.getElementById('lsPrevBtn').style.visibility = lessonIndex === 0 ? 'hidden' : 'visible';
    const nextBtn = document.getElementById('lsNextBtn');
    nextBtn.textContent = lessonIndex >= lessonWords.length - 1 ? '✅ Hoàn thành' : 'Tiếp ▶';
}

function nextLessonWord() { lessonIndex++; showLessonWord(); }
function prevLessonWord() { if (lessonIndex > 0) lessonIndex--; showLessonWord(); }

// Keyboard nav
document.addEventListener('keydown', e => {
    const lesson = document.getElementById('page-lesson');
    if (!lesson.classList.contains('active')) return;
    if (e.key === 'ArrowRight' || e.key === ' ') nextLessonWord();
    if (e.key === 'ArrowLeft') prevLessonWord();
});

// === REVIEW (Flashcard + SRS) ===
async function startReview() {
    const data = await api(`/api/review/${currentLevel}?limit=20`);
    if (!data || !data.words || data.words.length === 0) {
        alert('🎉 Không có từ cần ôn tập hôm nay!');
        return;
    }
    reviewWords = data.words;
    reviewIndex = 0;
    document.getElementById('startReviewBtn').style.display = 'none';
    document.getElementById('reviewContainer').style.display = 'block';
    document.getElementById('reviewDone').style.display = 'none';
    showReviewCard();
}

function loadReview() {
    document.getElementById('startReviewBtn').style.display = 'inline-block';
    document.getElementById('reviewContainer').style.display = 'none';
    document.getElementById('reviewDone').style.display = 'none';
    api('/api/stats').then(s => {
        if (s) document.getElementById('reviewCount').textContent = `(${s.due} từ cần ôn)`;
    });
}

async function showReviewCard() {
    if (reviewIndex >= reviewWords.length) {
        document.getElementById('reviewContainer').style.display = 'none';
        document.getElementById('reviewDone').style.display = 'block';
        return;
    }
    const w = reviewWords[reviewIndex];
    document.getElementById('fcChar').textContent = w.simplified;
    document.getElementById('fcPinyin').textContent = w.pinyin;
    document.getElementById('fcMeaning').textContent = w.meanings[0];
    document.getElementById('fcLevel').textContent = w.hsk_level;
    
    // Sino-Viet
    const svEl = document.getElementById('fcSinoViet');
    if (w.sino_viet) {
        svEl.textContent = 'Hán-Việt: ' + w.sino_viet;
        svEl.style.display = 'block';
    } else { svEl.style.display = 'none'; }
    
    // Sentences
    const se = document.getElementById('fcSentence'), sv = document.getElementById('fcSentenceVi');
    if (w.sentence_cn) {
        se.textContent = w.sentence_cn; se.style.display = 'block';
        sv.textContent = w.sentence_vi; sv.style.display = 'block';
    } else { se.style.display = 'none'; sv.style.display = 'none'; }
    
    // Context note
    const ctx = document.getElementById('fcContextNote');
    if (w.context_note) {
        ctx.textContent = '💡 ' + w.context_note;
        ctx.style.display = 'block';
    } else { ctx.style.display = 'none'; }
    
    document.getElementById('flashcard').classList.remove('flipped');
    document.getElementById('progressText').textContent = `${reviewIndex + 1}/${reviewWords.length}`;
    document.getElementById('progressFill').style.width = `${(reviewIndex / reviewWords.length) * 100}%`;
}

function flipCard() { document.getElementById('flashcard').classList.toggle('flipped'); }

async function submitReview(quality) {
    const w = reviewWords[reviewIndex];
    await api('/api/review', {
        method: 'POST',
        body: JSON.stringify({ word_id: w.id, quality })
    });
    reviewIndex++;
    showReviewCard();
}

// === WORDS LIST ===
async function loadWords() { await switchWordTab(currentLevel); }
async function switchWordTab(level) {
    currentLevel = level;
    document.querySelectorAll('.word-tabs .tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.word-tabs .tab')[level - 1].classList.add('active');
    const data = await api(`/api/words/${level}`);
    if (!data) return;
    const tbody = document.getElementById('wordTableBody');
    tbody.innerHTML = '';
    for (const w of data.words) {
        const sent = await api(`/api/sentence/${encodeURIComponent(w.simplified)}`);
        const s = sent && sent.cn ? `<span class="sent-cn">${sent.cn}</span><br><span class="sent-vi">${sent.vi}</span>` : '-';
        const sv = w.sino_viet || '-';
        tbody.innerHTML += `<tr onclick="showWordNote('${w.simplified}')"><td class="cn">${w.simplified}</td><td>${w.pinyin}</td><td>${w.meanings}</td><td>${sv}</td><td>${s}</td></tr>`;
    }
}

async function showWordNote(word) {
    const data = await api(`/api/note/${encodeURIComponent(word)}`);
    if (data && data.note) {
        alert(`💡 ${data.word}: ${data.note}`);
    }
}

// === DIALOGUES ===
async function loadDialogues() { await switchDlgTab(dialogueLevel); }
async function switchDlgTab(level) {
    dialogueLevel = level;
    document.querySelectorAll('.dlg-tabs .tab').forEach(t => t.classList.remove('active'));
    const tabs = document.querySelectorAll('.dlg-tabs .tab');
    if (level === 0) tabs[0].classList.add('active');
    else if (level === 1) tabs[1].classList.add('active');
    else tabs[2].classList.add('active');
    
    const data = level ? await api(`/api/dialogues?level=${level}`) : await api('/api/dialogues');
    if (!data || !data.dialogues) return;
    
    const list = document.getElementById('dlgList');
    list.innerHTML = '';
    data.dialogues.forEach(d => {
        const card = document.createElement('div');
        card.className = 'dlg-card';
        card.innerHTML = `
            <div class="dlg-card-title">${d.title}</div>
            <div class="dlg-card-context">${d.context || ''}</div>
            <div class="dlg-card-meta">
                <span class="dlg-badge">HSK ${d.hsk_level}</span>
                <span class="dlg-lines">${d.line_count} câu</span>
            </div>
        `;
        card.onclick = () => openDialogue(d.id);
        list.appendChild(card);
    });
}

async function openDialogue(dlgId) {
    const data = await api(`/api/dialogues/${dlgId}`);
    if (!data || !data.dialogue) return;
    
    document.getElementById('dlgTitle').textContent = data.dialogue.title;
    document.getElementById('dlgContext').textContent = '📍 ' + (data.dialogue.context || '');
    
    const chat = document.getElementById('dlgLines');
    chat.innerHTML = '';
    data.lines.forEach((l, i) => {
        const isA = l.speaker === 'A';
        const bubble = document.createElement('div');
        bubble.className = 'dlg-bubble ' + (isA ? 'dlg-a' : 'dlg-b');
        
        bubble.innerHTML = `
            <div class="dlg-speaker">${isA ? '👤 A' : '👤 B'}</div>
            <div class="dlg-cn" id="dlg-${l.id}" onclick="speak(this.textContent)">${l.simplified}</div>
            <div class="dlg-pinyin">${l.pinyin}</div>
            <div class="dlg-vi">${l.vietnamese}</div>
        `;
        chat.appendChild(bubble);
    });
    
    showPage('dialogue');
}

// === PROGRESS ===
async function loadProgress() {
    const data = await api('/api/progress');
    if (!data) return;
    const grid = document.getElementById('progressGrid');
    grid.innerHTML = '';
    data.levels.forEach(l => {
        const pct = l.total > 0 ? Math.round((l.mastered / l.total) * 100) : 0;
        grid.innerHTML += `
            <div class="progress-card">
                <h3>HSK ${l.hsk_level}</h3>
                <div class="progress-stat"><span class="progress-stat-label">Tổng</span><span class="progress-stat-value">${l.total}</span></div>
                <div class="progress-stat"><span class="progress-stat-label">Đã học</span><span class="progress-stat-value">${l.seen}</span></div>
                <div class="progress-stat"><span class="progress-stat-label">Thuộc</span><span class="progress-stat-value">${l.mastered} (${pct}%)</span></div>
                <div class="progress-stat"><span class="progress-stat-label">Độ chính xác</span><span class="progress-stat-value">${l.accuracy ? (l.accuracy*100).toFixed(0) : 0}%</span></div>
                <div class="progress-bar" style="margin-top:12px"><div class="progress-fill" style="width:${pct}%"></div></div>
            </div>`;
    });
    document.getElementById('progressDetail').innerHTML = `
        <div class="progress-card" style="margin-top:16px">
            <h3>Hôm nay</h3>
            <div class="progress-stat"><span class="progress-stat-label">Đã ôn</span><span class="progress-stat-value">${data.today_reviewed}</span></div>
        </div>`;
}

// Init
loadHome();
