package com.jamest9961.shortenglish.data

import android.content.Context
import android.content.SharedPreferences
import kotlinx.serialization.json.Json
import kotlin.random.Random

class SentenceRepository(private val context: Context) {

    private val prefs: SharedPreferences =
        context.getSharedPreferences("short_english_prefs", Context.MODE_PRIVATE)

    private val json = Json { ignoreUnknownKeys = true }

    var items: List<SentenceItem> = emptyList()
        private set

    private var itemsById: Map<Int, SentenceItem> = emptyMap()

    init {
        loadData()
    }

    private fun loadData() {
        try {
            val jsonString = context.assets.open("sentences_2500.json").bufferedReader().use { it.readText() }
            items = json.decodeFromString<List<SentenceItem>>(jsonString)
            itemsById = items.associateBy { it.id }
        } catch (e: Exception) {
            e.printStackTrace()
            items = emptyList()
        }
    }

    fun getTotalCount(): Int = items.size

    fun getItem(id: Int): SentenceItem {
        return itemsById[id] ?: items.firstOrNull() ?: SentenceItem(
            id = 1,
            en = "Enough is enough.",
            zh = "適可而止。",
            wordCount = 3,
            category = "🛑 拒絕終止",
            spkA = "👨 Kevin: He keeps playing loud music late at night despite multiple complaints.",
            spkB = "👩 Sarah: Enough is enough. We need to report this to the building manager.",
            note = "【核心含義】表達「適可而止」。\n【母語語用】屬於「🛑 拒絕終止」範疇。",
            litTrapZh = "足夠的就是足夠（中性描述數量充分）",
            chinglishTrapEn = "Enough is plenty.",
            spkAZh = "儘管屢遭投訴，他深夜依然大聲播放音樂。",
            spkBZh = "適可而止吧。我們必須向大樓管委會舉報這件事。"
        )
    }

    fun filterItems(category: String, query: String): List<SentenceItem> {
        var result = items
        if (category.isNotEmpty() && !category.startsWith("全部")) {
            result = result.filter { it.category == category }
        }
        if (query.isNotBlank()) {
            val q = query.trim().lowercase()
            result = result.filter {
                it.en.lowercase().contains(q) ||
                it.zh.lowercase().contains(q) ||
                it.id.toString() == q
            }
        }
        return result
    }

    // Bookmarks & Mastered (SharedPreferences persistence)
    fun isBookmarked(id: Int): Boolean {
        return prefs.getBoolean("bm_$id", false)
    }

    fun toggleBookmark(id: Int): Boolean {
        val current = isBookmarked(id)
        val newState = !current
        prefs.edit().putBoolean("bm_$id", newState).apply()
        return newState
    }

    fun getBookmarkedIds(): Set<Int> {
        return prefs.all.filter { it.key.startsWith("bm_") && it.value == true }
            .mapNotNull { it.key.removePrefix("bm_").toIntOrNull() }
            .toSet()
    }

    fun removeBookmarks(ids: Collection<Int>) {
        val editor = prefs.edit()
        ids.forEach { editor.remove("bm_$it") }
        editor.apply()
    }

    fun isMastered(id: Int): Boolean {
        return prefs.getBoolean("ms_$id", false)
    }

    fun toggleMastered(id: Int): Boolean {
        val current = isMastered(id)
        val newState = !current
        prefs.edit().putBoolean("ms_$id", newState).apply()
        return newState
    }

    fun getMasteredIds(): Set<Int> {
        return prefs.all.filter { it.key.startsWith("ms_") && it.value == true }
            .mapNotNull { it.key.removePrefix("ms_").toIntOrNull() }
            .toSet()
    }

    fun removeMastered(ids: Collection<Int>) {
        val editor = prefs.edit()
        ids.forEach { editor.remove("ms_$it") }
        editor.apply()
    }

    // Wrong Answers Persistence
    fun recordWrongAnswer(id: Int, isMode1: Boolean) {
        val key = if (isMode1) "wr1_$id" else "wr2_$id"
        prefs.edit().putBoolean(key, true).apply()
    }

    fun getWrongIdsMode1(): Set<Int> {
        return prefs.all.filter { it.key.startsWith("wr1_") && it.value == true }
            .mapNotNull { it.key.removePrefix("wr1_").toIntOrNull() }
            .toSet()
    }

    fun getWrongIdsMode2(): Set<Int> {
        return prefs.all.filter { it.key.startsWith("wr2_") && it.value == true }
            .mapNotNull { it.key.removePrefix("wr2_").toIntOrNull() }
            .toSet()
    }

    fun removeWrongs(ids: Collection<Int>) {
        val editor = prefs.edit()
        ids.forEach {
            editor.remove("wr1_$it")
            editor.remove("wr2_$it")
        }
        editor.apply()
    }

    // Mode 1: English Question -> Chinese Choices
    fun generateQuizMode1(itemId: Int): QuizQuestion {
        val target = getItem(itemId)
        val en = target.en
        val zh = target.zh

        val optCorrect = QuizChoice(
            text = zh,
            isCorrect = true,
            explanation = "【✅ 正確答案】「$en」是道地英語慣用語，意思就是「$zh」。"
        )

        val candidates = items.filter { it.id != target.id && it.zh != zh }
        val sample1 = candidates.filter { it.category == target.category }.randomOrNull() ?: candidates.random()
        val sample2 = candidates.filter { it.id != sample1.id && it.zh != sample1.zh }.random()

        val optConfuse1 = QuizChoice(
            text = sample1.zh,
            isCorrect = false,
            explanation = "【❌ 混淆選項】「${sample1.zh}」在道地英文中應表達為「${sample1.en}」，與本題「$en」不符。"
        )

        val optConfuse2 = QuizChoice(
            text = sample2.zh,
            isCorrect = false,
            explanation = "【❌ 混淆選項】「${sample2.zh}」在道地英文中對應的是「${sample2.en}」，並非本題的意思。"
        )

        val allChoices = listOf(optCorrect, optConfuse1, optConfuse2).shuffled()
        val correctIndex = allChoices.indexOfFirst { it.isCorrect }

        return QuizQuestion(
            id = target.id,
            type = QuizType.EN_TO_ZH,
            questionText = en,
            category = target.category,
            target = target,
            choices = allChoices,
            correctIndex = correctIndex
        )
    }

    // Mode 2: Chinese Question -> English Choices
    fun generateQuizMode2(itemId: Int): QuizQuestion {
        val target = getItem(itemId)
        val en = target.en
        val zh = target.zh

        val optCorrect = QuizChoice(
            text = en,
            isCorrect = true,
            explanation = "【✅ 正確答案】「$en」是母語者最道地自然、合乎文化習慣的表達方式，準確傳達「$zh」。"
        )

        val candidates = items.filter { it.id != target.id && it.en != en }
        val sample1 = candidates.filter { it.category == target.category }.randomOrNull() ?: candidates.random()
        val sample2 = candidates.filter { it.id != sample1.id && it.en != sample1.en }.random()

        val optConfuse1 = QuizChoice(
            text = sample1.en,
            isCorrect = false,
            explanation = "【❌ 混淆選項】「${sample1.en}」在母語中的實際含義是「${sample1.zh}」，不能用來表達本題要求的「$zh」。"
        )

        val optConfuse2 = QuizChoice(
            text = sample2.en,
            isCorrect = false,
            explanation = "【❌ 混淆選項】「${sample2.en}」在母語中的實際含義是「${sample2.zh}」，完全偏離了題目情境。"
        )

        val allChoices = listOf(optCorrect, optConfuse1, optConfuse2).shuffled()
        val correctIndex = allChoices.indexOfFirst { it.isCorrect }

        return QuizQuestion(
            id = target.id,
            type = QuizType.ZH_TO_EN,
            questionText = zh,
            category = target.category,
            target = target,
            choices = allChoices,
            correctIndex = correctIndex
        )
    }

    // Persistence for Last Used Page / Screen State
    fun getLastTabName(): String {
        return prefs.getString("last_tab_name", "TEXTBOOK") ?: "TEXTBOOK"
    }

    fun setLastTabName(tabName: String) {
        prefs.edit().putString("last_tab_name", tabName).apply()
    }

    fun getLastTextbookId(): Int {
        val total = items.size.coerceAtLeast(1)
        return prefs.getInt("last_textbook_id", 1).coerceIn(1, total)
    }

    fun setLastTextbookId(id: Int) {
        val total = items.size.coerceAtLeast(1)
        prefs.edit().putInt("last_textbook_id", id.coerceIn(1, total)).apply()
    }

    fun getLastCategory(): String {
        return prefs.getString("last_category", "全部(2500題.左右移)") ?: "全部(2500題.左右移)"
    }

    fun setLastCategory(category: String) {
        prefs.edit().putString("last_category", category).apply()
    }

    fun getLastNotebookTab(): String {
        return prefs.getString("last_notebook_tab", "BOOKMARKS") ?: "BOOKMARKS"
    }

    fun setLastNotebookTab(tabName: String) {
        prefs.edit().putString("last_notebook_tab", tabName).apply()
    }
}
