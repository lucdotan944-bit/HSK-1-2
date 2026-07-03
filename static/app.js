// Hán Ngữ+ — Frontend App Logic
let currentLevel = 1;
let reviewWords = [];
let reviewIndex = 0;
let dialogueLevel = 0;

// Lesson state
let lessonWords = [];
let lessonIndex = 0;
let currentThemeId = null;

// Pronunciation check (Web Speech Recognition — Chrome/Edge)
const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
const speechRecognitionSupported = !!SpeechRec;

function scorePronunciation(target, recognized) {
    // So khớp ký tự hanzi (không phải phân tích ngữ âm): đúng hết=ok, >=60% trùng=warn
    const t = (target.match(/[一-鿿]/g) || []).join('');
    const r = (recognized.match(/[一-鿿]/g) || []).join('');
    if (t === r) return 'ok';
    if (t.length === 0) return 'fail';
    let overlap = 0;
    const rChars = r.split('');
    for (const ch of t) {
        const i = rChars.indexOf(ch);
        if (i >= 0) { overlap++; rChars.splice(i, 1); }
    }
    return overlap / t.length >= 0.6 ? 'warn' : 'fail';
}

function startPronunciationCheck(btn, targetText, wordId = null) {
    if (!speechRecognitionSupported) return;
    const resultEl = btn.parentElement.querySelector('.pron-result');
    const rec = new SpeechRec();
    rec.lang = 'zh-CN';
    rec.interimResults = false;
    rec.maxAlternatives = 1;

    btn.classList.add('listening');
    btn.textContent = '🎙️...';
    if (resultEl) { resultEl.textContent = ''; resultEl.className = 'pron-result'; }

    rec.onresult = (e) => {
        const recognized = e.results[0][0].transcript;
        const score = scorePronunciation(targetText, recognized);
        if (resultEl) {
            const icons = { ok: '✅', warn: '⚠️', fail: '❌' };
            resultEl.textContent = `${icons[score]} Nghe được: "${recognized}"`;
            resultEl.className = 'pron-result ' + score;
        }
        // fire-and-forget
        api('/api/pronunciation/log', {
            method: 'POST',
            body: JSON.stringify({ word_id: wordId, target_text: targetText, recognized_text: recognized, score })
        });
    };
    rec.onerror = (e) => {
        if (resultEl) {
            resultEl.textContent = e.error === 'no-speech' ? '🔇 Không nghe thấy gì, thử lại' : '⚠️ Lỗi micro';
            resultEl.className = 'pron-result warn';
        }
    };
    rec.onend = () => {
        btn.classList.remove('listening');
        btn.textContent = '🎤';
    };
    rec.start();
}

// Audio
function speak(text, rate = 0.85) {
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'zh-CN'; u.rate = rate; u.pitch = 1.0;
    window.speechSynthesis.speak(u);
}
function playReviewAudio(e) { e.stopPropagation(); const el = document.getElementById('fcChar'); if(el) speak(el.textContent); }
function playLessonAudio() { const el = document.getElementById('lsChar'); if(el) speak(el.textContent); }
function checkReviewPronunciation(e, btn) {
    e.stopPropagation();
    const w = reviewWords[reviewIndex];
    if (w) startPronunciationCheck(btn, w.simplified, w.id);
}
function checkLessonPronunciation(btn) {
    const w = lessonWords[lessonIndex];
    if (w) startPronunciationCheck(btn, w.simplified, w.id);
}
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
    if (page === 'writing') loadWritingChars();
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

// === GAMIFICATION ===
let badgeCatalog = null;
async function getBadgeCatalog() {
    if (!badgeCatalog) {
        const data = await api('/api/badges');
        badgeCatalog = {};
        if (data && data.badges) data.badges.forEach(b => badgeCatalog[b.badge_id] = b);
    }
    return badgeCatalog;
}

async function loadGamifyState() {
    const state = await api('/api/gamify/state');
    if (!state) return;
    const xpEl = document.getElementById('statXp');
    const stEl = document.getElementById('statStreak');
    if (xpEl) xpEl.textContent = state.xp;
    if (stEl) stEl.textContent = state.current_streak;

    // Banner mời làm placement test: người mới (XP=0, chưa test, chưa bỏ qua)
    const banner = document.getElementById('placementBanner');
    const dismissed = localStorage.getItem('placementDismissed');
    banner.style.display =
        (state.xp === 0 && state.placement_level === 0 && !dismissed) ? 'flex' : 'none';
}

function dismissPlacementBanner() {
    localStorage.setItem('placementDismissed', '1');
    document.getElementById('placementBanner').style.display = 'none';
}

// === PLACEMENT TEST ===
let placementQuestions = [];
let placementIndex = 0;
let placementAnswers = [];

async function startPlacementTest() {
    const data = await api('/api/quiz/choices/2?count=15');
    if (!data || !data.questions || data.questions.length === 0) return;
    placementQuestions = data.questions;
    placementIndex = 0;
    placementAnswers = [];
    document.getElementById('placementQuiz').style.display = 'block';
    document.getElementById('placementDone').style.display = 'none';
    showPage('placement');
    showPlacementQuestion();
}

function showPlacementQuestion() {
    if (placementIndex >= placementQuestions.length) {
        finishPlacementTest();
        return;
    }
    const q = placementQuestions[placementIndex];
    document.getElementById('placementProgress').textContent =
        `${placementIndex + 1}/${placementQuestions.length}`;
    document.getElementById('plChar').textContent = q.simplified;
    document.getElementById('plPinyin').textContent = q.pinyin;
    const box = document.getElementById('plChoices');
    box.innerHTML = '';
    q.choices.forEach(choice => {
        const btn = document.createElement('button');
        btn.className = 'quiz-choice';
        btn.textContent = choice;
        btn.onclick = () => {
            const correct = choice === q.correct_meaning;
            placementAnswers.push({ word_id: q.word_id, hsk_level: q.hsk_level, correct });
            document.querySelectorAll('#plChoices .quiz-choice').forEach(b => {
                b.disabled = true;
                if (b.textContent === q.correct_meaning) b.classList.add('correct');
            });
            if (!correct) btn.classList.add('wrong');
            setTimeout(() => { placementIndex++; showPlacementQuestion(); }, correct ? 600 : 1400);
        };
        box.appendChild(btn);
    });
}

async function finishPlacementTest() {
    const r = await api('/api/placement/submit', {
        method: 'POST',
        body: JSON.stringify({ answers: placementAnswers })
    });
    document.getElementById('placementQuiz').style.display = 'none';
    document.getElementById('placementDone').style.display = 'block';
    if (r) {
        showBadgeToast(r.newly_earned_badges);
        const pct = Math.round(r.accuracy * 100);
        document.getElementById('plResultText').innerHTML =
            `Bạn trả lời đúng <b>${pct}%</b>.<br>Gợi ý: bắt đầu học từ <b>HSK ${r.recommended_level}</b>.` +
            (r.recommended_level === 2
                ? ' Bạn đã nắm vững nền tảng HSK 1!'
                : ' Hãy học chắc các chủ đề HSK 1 trước nhé.');
    }
    localStorage.setItem('placementDismissed', '1');
}

async function showBadgeToast(badgeIds) {
    if (!badgeIds || badgeIds.length === 0) return;
    const catalog = await getBadgeCatalog();
    const toast = document.getElementById('badgeToast');
    const b = catalog[badgeIds[0]];
    toast.innerHTML = `<span class="badge-toast-icon">${b ? b.icon : '🏅'}</span>
        <div><div class="badge-toast-title">Huy hiệu mới!</div>
        <div class="badge-toast-name">${b ? b.name : badgeIds[0]}</div></div>`;
    toast.style.display = 'flex';
    setTimeout(() => { toast.style.display = 'none'; }, 3500);
}

// === HOME: Clickable Theme Cards ===
async function loadHome() {
    const [stats, themes] = await Promise.all([
        api('/api/stats'),
        api('/api/themes')
    ]);
    loadGamifyState();
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
    document.getElementById('lessonQuiz').style.display = 'none';
    showLessonWord();
    showPage('lesson');
}

function showLessonWord() {
    if (lessonIndex >= lessonWords.length) {
        document.getElementById('lessonContent').style.display = 'none';
        startThemeQuiz();
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
        api(`/api/themes/${currentThemeId}/learn/${w.id}`, { method: 'POST' })
            .then(r => { if (r) showBadgeToast(r.newly_earned_badges); });
        w.learned = true;
    }
    
    // Nav buttons
    document.getElementById('lsPrevBtn').style.visibility = lessonIndex === 0 ? 'hidden' : 'visible';
    const nextBtn = document.getElementById('lsNextBtn');
    nextBtn.textContent = lessonIndex >= lessonWords.length - 1 ? '✅ Hoàn thành' : 'Tiếp ▶';
}

function nextLessonWord() { lessonIndex++; showLessonWord(); }
function prevLessonWord() { if (lessonIndex > 0) lessonIndex--; showLessonWord(); }

// === LESSON MINI-QUIZ ===
let quizQuestions = [];
let quizIndex = 0;
let quizResults = [];

async function startThemeQuiz() {
    const count = Math.min(5, lessonWords.length);
    const data = await api(`/api/quiz/choices/2?count=${count}&theme_id=${currentThemeId}`);
    if (!data || !data.questions || data.questions.length === 0) {
        finishLesson(null);
        return;
    }
    quizQuestions = data.questions;
    quizIndex = 0;
    quizResults = [];
    document.getElementById('lessonQuiz').style.display = 'block';
    showQuizQuestion();
}

function showQuizQuestion() {
    if (quizIndex >= quizQuestions.length) {
        submitThemeQuiz();
        return;
    }
    const q = quizQuestions[quizIndex];
    document.getElementById('quizProgress').textContent = `Câu ${quizIndex + 1}/${quizQuestions.length}`;
    document.getElementById('quizChar').textContent = q.simplified;
    document.getElementById('quizPinyin').textContent = q.pinyin;
    const box = document.getElementById('quizChoices');
    box.innerHTML = '';
    q.choices.forEach(choice => {
        const btn = document.createElement('button');
        btn.className = 'quiz-choice';
        btn.textContent = choice;
        btn.onclick = () => answerQuizQuestion(btn, choice, q);
        box.appendChild(btn);
    });
    speak(q.simplified);
}

function answerQuizQuestion(btn, choice, q) {
    const correct = choice === q.correct_meaning;
    quizResults.push({ word_id: q.word_id, correct });
    document.querySelectorAll('.quiz-choice').forEach(b => {
        b.disabled = true;
        if (b.textContent === q.correct_meaning) b.classList.add('correct');
    });
    if (!correct) btn.classList.add('wrong');
    setTimeout(() => { quizIndex++; showQuizQuestion(); }, correct ? 700 : 1500);
}

async function submitThemeQuiz() {
    document.getElementById('lessonQuiz').style.display = 'none';
    const r = await api('/api/quiz/theme-result', {
        method: 'POST',
        body: JSON.stringify({ theme_id: currentThemeId, results: quizResults })
    });
    if (r) showBadgeToast(r.newly_earned_badges);
    finishLesson(r);
}

async function finishLesson(quizResult) {
    document.getElementById('lessonDone').style.display = 'block';
    document.getElementById('lessonSummary').textContent =
        `Bạn đã học ${lessonWords.length} từ trong chủ đề này.`;

    const scoreEl = document.getElementById('lessonQuizScore');
    if (quizResult && quizResult.total > 0) {
        scoreEl.innerHTML = `<div class="quiz-score">📝 Mini-quiz: <b>${quizResult.correct}/${quizResult.total}</b> câu đúng</div>`;
    } else {
        scoreEl.innerHTML = '';
    }

    // Gợi ý hội thoại liên quan (chung từ vựng với theme)
    const suggEl = document.getElementById('lessonSuggestDialogue');
    suggEl.innerHTML = '';
    const rel = await api(`/api/themes/${currentThemeId}/related-dialogues`);
    if (rel && rel.dialogues && rel.dialogues.length > 0) {
        const d = rel.dialogues[0];
        suggEl.innerHTML = `
            <div class="dlg-suggest-card" onclick="openDialogue('${d.id}')">
                <div class="dlg-suggest-label">💬 Hội thoại gợi ý — dùng ${d.shared_words} từ bạn vừa học</div>
                <div class="dlg-suggest-title">${d.title}</div>
                <div class="dlg-suggest-context">${d.context || ''}</div>
            </div>`;
    }
}

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
    const r = await api('/api/review', {
        method: 'POST',
        body: JSON.stringify({ word_id: w.id, quality })
    });
    if (r) showBadgeToast(r.newly_earned_badges);
    reviewIndex++;
    showReviewCard();
}

// === WRITING PRACTICE (HanziWriter) ===
let writingLevel = 1;
let writingChars = [];
let currentWriter = null;
let currentWritingChar = null;

async function loadWritingChars() { await switchWritingTab(writingLevel); }

async function switchWritingTab(level) {
    writingLevel = level;
    document.querySelectorAll('#page-writing .word-tabs .tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('#page-writing .word-tabs .tab')[level - 1].classList.add('active');
    document.getElementById('writingGridView').style.display = 'block';
    document.getElementById('writingPracticeView').style.display = 'none';

    const data = await api(`/api/writing/characters?hsk_level=${level}`);
    if (!data) return;
    writingChars = data.characters.filter(c => c.hsk_level === level);

    const grid = document.getElementById('writingCharGrid');
    grid.innerHTML = '';
    writingChars.forEach(c => {
        const chip = document.createElement('div');
        chip.className = 'writing-char-chip'
            + (c.mastered ? ' mastered' : (c.practiced ? ' practiced' : ''));
        chip.textContent = c.character;
        chip.title = c.mastered ? 'Đã thành thạo (viết đúng 100%)'
            : (c.practiced ? `Đã luyện ${c.attempts} lần` : 'Chưa luyện');
        chip.onclick = () => openWritingPractice(c.character);
        grid.appendChild(chip);
    });
}

function openWritingPractice(char) {
    currentWritingChar = char;
    document.getElementById('writingGridView').style.display = 'none';
    document.getElementById('writingPracticeView').style.display = 'block';
    document.getElementById('writingCharTitle').textContent = char;
    document.getElementById('writingResult').innerHTML = '';
    document.getElementById('writingStatus').textContent = '';

    // Từ chứa ký tự này + pinyin/nghĩa để có ngữ cảnh
    api(`/api/words/${writingLevel}`).then(data => {
        if (!data) return;
        const w = data.words.find(w => w.simplified.includes(char));
        document.getElementById('writingWordInfo').innerHTML = w
            ? `<span class="wi-pinyin">${w.pinyin}</span> — ${w.meanings}${w.sino_viet ? ` <span class="wi-sino">(${w.sino_viet})</span>` : ''}`
            : '';
    });

    document.getElementById('hanziTarget').innerHTML = '';
    currentWriter = HanziWriter.create('hanziTarget', char, {
        width: 240, height: 240, padding: 12,
        strokeColor: '#1D3557', outlineColor: '#DEE2E6',
        showCharacter: true, showOutline: true,
        strokeAnimationSpeed: 1, delayBetweenStrokes: 200,
    });
}

function closeWritingPractice() {
    currentWriter = null;
    switchWritingTab(writingLevel);
}

function animateCharacter() {
    if (!currentWriter) return;
    document.getElementById('writingResult').innerHTML = '';
    document.getElementById('writingStatus').textContent = 'Xem cách viết';
    currentWriter.showCharacter();
    currentWriter.animateCharacter();
}

function startWritingQuiz() {
    if (!currentWriter) return;
    document.getElementById('writingResult').innerHTML = '';
    document.getElementById('writingStatus').textContent = 'Vẽ từng nét theo thứ tự';
    currentWriter.quiz({
        showOutline: true,
        onComplete: async (summary) => {
            const mistakes = summary.totalMistakes;
            const r = await api('/api/writing/complete', {
                method: 'POST',
                body: JSON.stringify({ character: currentWritingChar, mistakes })
            });
            if (r) showBadgeToast(r.newly_earned_badges);
            const resEl = document.getElementById('writingResult');
            if (mistakes === 0) {
                resEl.innerHTML = '<div class="writing-perfect">🎉 Hoàn hảo! Không sai nét nào (+30 XP)</div>';
            } else {
                resEl.innerHTML = `<div class="writing-ok">✅ Hoàn thành — sai ${mistakes} nét (+15 XP). Thử lại để đạt hoàn hảo!</div>`;
            }
            document.getElementById('writingStatus').textContent = '';
        }
    });
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
            <div class="dlg-pron-row">
                <button class="btn-mic-sm btn-mic" onclick="startPronunciationCheck(this, document.getElementById('dlg-${l.id}').textContent)">🎤 Nói thử</button>
                <span class="pron-result"></span>
            </div>
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
    loadBadgeGrid();
}

async function loadBadgeGrid() {
    const data = await api('/api/badges');
    if (!data || !data.badges) return;
    const grid = document.getElementById('badgeGrid');
    grid.innerHTML = '';
    data.badges.forEach(b => {
        grid.innerHTML += `
            <div class="badge-card${b.earned ? '' : ' locked'}" title="${b.desc}">
                <div class="badge-card-icon">${b.icon}</div>
                <div class="badge-card-name">${b.name}</div>
                <div class="badge-card-desc">${b.desc}</div>
            </div>`;
    });
}

// Init
if (!speechRecognitionSupported) document.body.classList.add('no-speech-rec');
loadHome();
