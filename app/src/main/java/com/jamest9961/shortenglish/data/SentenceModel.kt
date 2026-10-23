package com.jamest9961.shortenglish.data

import kotlinx.serialization.Serializable

@Serializable
data class SentenceItem(
    val id: Int,
    val en: String,
    val zh: String,
    val wordCount: Int,
    val category: String,
    val spkA: String,
    val spkB: String,
    val note: String,
    val litTrapZh: String,
    val chinglishTrapEn: String,
    val spkAZh: String = "",
    val spkBZh: String = ""
)

enum class QuizType {
    EN_TO_ZH, // 模式一: 英文出題，中文選答
    ZH_TO_EN  // 模式二: 中文出題，英文選答
}

data class QuizChoice(
    val text: String,
    val isCorrect: Boolean,
    val explanation: String
)

data class QuizQuestion(
    val id: Int,
    val type: QuizType,
    val questionText: String,
    val category: String,
    val target: SentenceItem,
    val choices: List<QuizChoice>,
    val correctIndex: Int
)
