package com.jamest9961.shortenglish.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.jamest9961.shortenglish.data.QuizQuestion
import com.jamest9961.shortenglish.data.QuizType
import com.jamest9961.shortenglish.data.SentenceRepository
import com.jamest9961.shortenglish.sound.TtsManager

@Composable
fun QuizScreen(
    initialQuizType: QuizType = QuizType.EN_TO_ZH,
    repository: SentenceRepository,
    ttsManager: TtsManager,
    onBackToTextbook: () -> Unit
) {
    var quizType by remember(initialQuizType) { mutableStateOf(initialQuizType) }

    var currentQuestion by remember(quizType) {
        val randId = (1..repository.getTotalCount()).random()
        mutableStateOf(
            if (quizType == QuizType.EN_TO_ZH) repository.generateQuizMode1(randId)
            else repository.generateQuizMode2(randId)
        )
    }

    var selectedIndex by remember(currentQuestion) { mutableStateOf<Int?>(null) }
    var scoreCorrect by remember(quizType) { mutableStateOf(0) }
    var scoreTotal by remember(quizType) { mutableStateOf(0) }
    var streak by remember(quizType) { mutableStateOf(0) }

    val answered = selectedIndex != null
    val isCorrect = selectedIndex == currentQuestion.correctIndex

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF0B0F19))
            .padding(horizontal = 8.dp, vertical = 2.dp)
    ) {
        // 1. Top Compact Header with [ ◀ 回到上一階 ] (緊湊上下間距)
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(6.dp))
                .background(Color(0xFF131B2E))
                .padding(horizontal = 6.dp, vertical = 2.dp),
            horizontalArrangement = Arrangement.Start,
            verticalAlignment = Alignment.CenterVertically
        ) {
            // 回到上一階按鈕 (極致緊湊高度)
            Button(
                onClick = {
                    if (quizType == QuizType.ZH_TO_EN) {
                        // 模式二回到上一階 (回到模式一)
                        quizType = QuizType.EN_TO_ZH
                        selectedIndex = null
                    } else {
                        // 模式一回到上一階 (回到課本研讀)
                        onBackToTextbook()
                    }
                },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF334155)),
                shape = RoundedCornerShape(5.dp),
                contentPadding = PaddingValues(horizontal = 6.dp, vertical = 0.dp),
                modifier = Modifier.height(25.dp)
            ) {
                Text("◀ 回到上一階", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = Color(0xFFF1F5F9))
            }

            Spacer(modifier = Modifier.width(6.dp))

            // 英文題 / 中文題 模式切換按鈕
            Row(
                modifier = Modifier
                    .clip(RoundedCornerShape(5.dp))
                    .background(Color(0xFF0F172A))
                    .border(1.dp, Color(0xFF1E293B), RoundedCornerShape(5.dp))
                    .padding(1.dp),
                horizontalArrangement = Arrangement.spacedBy(1.dp)
            ) {
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(4.dp))
                        .background(if (quizType == QuizType.EN_TO_ZH) Color(0xFF2563EB) else Color.Transparent)
                        .clickable {
                            if (quizType != QuizType.EN_TO_ZH) {
                                quizType = QuizType.EN_TO_ZH
                                selectedIndex = null
                            }
                        }
                        .padding(horizontal = 6.dp, vertical = 2.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "英文題",
                        fontSize = 10.5.sp,
                        fontWeight = if (quizType == QuizType.EN_TO_ZH) FontWeight.Bold else FontWeight.Medium,
                        color = if (quizType == QuizType.EN_TO_ZH) Color.White else Color(0xFF94A3B8)
                    )
                }

                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(4.dp))
                        .background(if (quizType == QuizType.ZH_TO_EN) Color(0xFF2563EB) else Color.Transparent)
                        .clickable {
                            if (quizType != QuizType.ZH_TO_EN) {
                                quizType = QuizType.ZH_TO_EN
                                selectedIndex = null
                            }
                        }
                        .padding(horizontal = 6.dp, vertical = 2.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "中文題",
                        fontSize = 10.5.sp,
                        fontWeight = if (quizType == QuizType.ZH_TO_EN) FontWeight.Bold else FontWeight.Medium,
                        color = if (quizType == QuizType.ZH_TO_EN) Color.White else Color(0xFF94A3B8)
                    )
                }
            }

            Spacer(modifier = Modifier.width(6.dp))

            Text(
                text = "[${currentQuestion.category}]",
                fontSize = 10.5.sp,
                color = Color(0xFFA5B4FC),
                modifier = Modifier
                    .background(Color(0xFF312E81), RoundedCornerShape(4.dp))
                    .padding(horizontal = 5.dp, vertical = 2.dp)
            )
        }

        Spacer(modifier = Modifier.height(2.dp))

        // 2. Compact Question Card with Inline TTS Audio Button
        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(10.dp),
            colors = CardDefaults.cardColors(containerColor = Color(0xFF131B2E)),
            border = CardDefaults.outlinedCardBorder().copy(brush = androidx.compose.ui.graphics.SolidColor(Color(0xFF1E293B)))
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 12.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = if (quizType == QuizType.EN_TO_ZH) "請選出道地中文釋義：" else "請選出道地短成語：",
                        fontSize = 11.sp,
                        color = Color(0xFF94A3B8)
                    )
                    Spacer(modifier = Modifier.height(2.dp))
                    Text(
                        text = currentQuestion.questionText,
                        fontSize = if (quizType == QuizType.EN_TO_ZH) 22.sp else 19.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White,
                        lineHeight = 26.sp,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                }

                Spacer(modifier = Modifier.width(8.dp))

                val isTtsEnabled = (quizType == QuizType.EN_TO_ZH || answered)

                Button(
                    onClick = {
                        val speechText = if (quizType == QuizType.EN_TO_ZH)
                            currentQuestion.questionText
                        else
                            currentQuestion.target.en
                        ttsManager.speak(speechText, slow = false)
                    },
                    enabled = isTtsEnabled,
                    colors = ButtonDefaults.buttonColors(
                        containerColor = Color(0xFF2563EB),
                        contentColor = Color.White,
                        disabledContainerColor = Color(0xFF1E293B),
                        disabledContentColor = Color(0xFF64748B)
                    ),
                    border = if (!isTtsEnabled) BorderStroke(1.dp, Color(0xFF334155)) else null,
                    shape = RoundedCornerShape(8.dp),
                    contentPadding = PaddingValues(horizontal = 10.dp, vertical = 6.dp),
                    modifier = Modifier.height(36.dp)
                ) {
                    Text("🔊 發音", fontSize = 11.sp, fontWeight = FontWeight.Bold)
                }
            }
        }

        Spacer(modifier = Modifier.height(6.dp))

        // 3. 4 Options: Adaptive Compact Height, Soft Pastel Right/Wrong colors
        Column(
            modifier = Modifier.fillMaxWidth(),
            verticalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            currentQuestion.choices.forEachIndexed { idx, choice ->
                val letter = ('A' + idx)
                val isSelectedChoice = (selectedIndex == idx)
                val isCorrectChoice = (idx == currentQuestion.correctIndex)

                val bgColor: Color
                val borderColor: Color
                val textColor: Color
                val prefix: String

                if (!answered) {
                    bgColor = Color(0xFF131B2E)
                    borderColor = Color(0xFF1E293B)
                    textColor = Color(0xFFE2E8F0)
                    prefix = "$letter."
                } else {
                    if (isCorrectChoice) {
                        // 淡薄荷綠 Pastel Mint Green (對的背景色淡、字體清晰極易辨識)
                        bgColor = Color(0xFF063327)
                        borderColor = Color(0xFF10B981)
                        textColor = Color(0xFFECFDF5)
                        prefix = "✓ $letter."
                    } else if (isSelectedChoice && !isCorrect) {
                        // 淡玫瑰紅 Pastel Rose Red (錯的背景色淡、字體清晰極易辨識)
                        bgColor = Color(0xFF3B0F13)
                        borderColor = Color(0xFFEF4444)
                        textColor = Color(0xFFFEF2F2)
                        prefix = "✗ $letter."
                    } else {
                        bgColor = Color(0xFF0F172A)
                        borderColor = Color(0xFF1E293B)
                        textColor = Color(0xFF64748B)
                        prefix = "  $letter."
                    }
                }

                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(8.dp))
                        .background(bgColor)
                        .border(
                            width = if (answered && (isCorrectChoice || isSelectedChoice)) 2.dp else 1.dp,
                            color = borderColor,
                            shape = RoundedCornerShape(8.dp)
                        )
                        .clickable(enabled = !answered) {
                            selectedIndex = idx
                            scoreTotal += 1
                            if (idx == currentQuestion.correctIndex) {
                                scoreCorrect += 1
                                streak += 1
                            } else {
                                streak = 0
                                repository.recordWrongAnswer(currentQuestion.id, quizType == QuizType.EN_TO_ZH)
                            }
                        }
                        .padding(horizontal = 10.dp, vertical = 7.dp)
                ) {
                    Text(
                        text = "$prefix  ${choice.text}",
                        fontSize = 13.5.sp,
                        fontWeight = if (answered && (isCorrectChoice || isSelectedChoice)) FontWeight.Bold else FontWeight.Medium,
                        color = textColor,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(4.dp))

        // 4. Adaptive Result & Explanation Area (weight 1f: fits within screen automatically!)
        Box(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth()
        ) {
            if (answered) {
                Card(
                    modifier = Modifier.fillMaxSize(),
                    shape = RoundedCornerShape(10.dp),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFF131B2E)),
                    border = CardDefaults.outlinedCardBorder().copy(brush = androidx.compose.ui.graphics.SolidColor(Color(0xFF1E293B)))
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(horizontal = 10.dp, vertical = 8.dp)
                            .verticalScroll(rememberScrollState())
                    ) {
                        // Result Banner
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(6.dp))
                                .background(if (isCorrect) Color(0xFF064E3B) else Color(0xFF450A0A))
                                .border(1.dp, if (isCorrect) Color(0xFF10B981) else Color(0xFFEF4444), RoundedCornerShape(6.dp))
                                .padding(horizontal = 10.dp, vertical = 6.dp)
                        ) {
                            Text(
                                text = if (isCorrect)
                                    "🎉 答對了！恭喜！"
                                else
                                    "❌ 答錯了！正解為 [${'A' + currentQuestion.correctIndex}]（已記入錯題本）",
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (isCorrect) Color(0xFFA7F3D0) else Color(0xFFFECACA)
                            )
                        }

                        Spacer(modifier = Modifier.height(6.dp))

                        Text(
                            text = "📖 各選項深度剖析：",
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFFFBBF24)
                        )

                        Spacer(modifier = Modifier.height(4.dp))

                        currentQuestion.choices.forEachIndexed { idx, ch ->
                            val mark = if (ch.isCorrect) "✅ 正解" else "❌ 陷阱"
                            Text(
                                text = "[${'A' + idx}] ($mark) ${ch.text}",
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (ch.isCorrect) Color(0xFF34D399) else Color(0xFFF87171)
                            )
                            Text(
                                text = "    ↳ ${ch.explanation}",
                                fontSize = 11.sp,
                                color = Color(0xFFCBD5E1),
                                lineHeight = 15.sp,
                                modifier = Modifier.padding(bottom = 3.dp)
                            )
                        }

                        Spacer(modifier = Modifier.height(4.dp))

                        // Example sentence containing the short expression (only sentence 2, no speaker name) + TTS button
                        val rawB = currentQuestion.target.spkB
                        val exampleEn = if (rawB.contains(":")) rawB.substringAfter(":").trim() else rawB
                        val exampleZh = currentQuestion.target.spkBZh

                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(8.dp))
                                .background(Color(0xFF0F172A))
                                .border(1.dp, Color(0xFF1E293B), RoundedCornerShape(8.dp))
                                .padding(horizontal = 10.dp, vertical = 7.dp)
                        ) {
                            Column {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        text = "💬 應用例句：",
                                        fontSize = 11.5.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = Color(0xFF38BDF8)
                                    )

                                    Button(
                                        onClick = {
                                            ttsManager.speak(exampleEn, slow = false)
                                        },
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0284C7)),
                                        shape = RoundedCornerShape(6.dp),
                                        contentPadding = PaddingValues(horizontal = 10.dp, vertical = 0.dp),
                                        modifier = Modifier.height(26.dp)
                                    ) {
                                        Text("🔊 例句發音", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color.White)
                                    }
                                }

                                Spacer(modifier = Modifier.height(4.dp))

                                Text(
                                    text = exampleEn,
                                    fontSize = 13.sp,
                                    fontWeight = FontWeight.SemiBold,
                                    color = Color(0xFF60A5FA),
                                    lineHeight = 17.sp
                                )

                                if (exampleZh.isNotBlank()) {
                                    Spacer(modifier = Modifier.height(2.dp))
                                    Text(
                                        text = if (exampleZh.startsWith("（") || exampleZh.startsWith("("))
                                            exampleZh
                                        else
                                            "（$exampleZh）",
                                        fontSize = 11.5.sp,
                                        color = Color(0xFF93C5FD),
                                        lineHeight = 15.sp
                                    )
                                }
                            }
                        }
                    }
                }
            } else {
                // Subtle prompt box while waiting for user to choose
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .clip(RoundedCornerShape(10.dp))
                        .background(Color(0xFF131B2E).copy(alpha = 0.5f))
                        .border(1.dp, Color(0xFF1E293B), RoundedCornerShape(10.dp)),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "💡 請點擊上方選項作答，考驗您的母語思維直覺！",
                        fontSize = 12.sp,
                        color = Color(0xFF64748B)
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(6.dp))

        // 5. Docked Next Button (Always on screen!)
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(8.dp))
                .background(Color(0xFF131B2E))
                .padding(horizontal = 8.dp, vertical = 6.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "單字長度: ${currentQuestion.target.wordCount} 字 (6字以內)",
                fontSize = 11.sp,
                color = Color(0xFF94A3B8)
            )

            Button(
                onClick = {
                    val randId = (1..repository.getTotalCount()).random()
                    currentQuestion = if (quizType == QuizType.EN_TO_ZH)
                        repository.generateQuizMode1(randId)
                    else
                        repository.generateQuizMode2(randId)
                    selectedIndex = null
                },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2563EB)),
                shape = RoundedCornerShape(8.dp),
                contentPadding = PaddingValues(horizontal = 20.dp, vertical = 6.dp),
                modifier = Modifier.height(38.dp)
            ) {
                Text("下一題 ▶", fontSize = 13.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}
