package com.jamest9961.shortenglish.ui

import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import android.app.Activity
import android.content.Context
import android.view.inputmethod.InputMethodManager
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.jamest9961.shortenglish.data.SentenceItem
import com.jamest9961.shortenglish.data.SentenceRepository
import com.jamest9961.shortenglish.sound.TtsManager

val CATEGORIES = listOf(
    "全部(2500題.左右移)",
    "🛑 拒絕終止",
    "⚡ 質疑反對",
    "🤝 贊同承諾",
    "🔥 情緒感嘆",
    "🎯 處世智慧",
    "💡 勸告提醒",
    "💼 職場應對",
    "💬 社交客套",
    "🌟 鼓舞激勵",
    "⚖️ 認同妥協",
    "⏳ 時機狀態",
    "🗣️ 日常口語"
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TextbookScreen(
    repository: SentenceRepository,
    ttsManager: TtsManager,
    currentId: Int,
    onIdChanged: (Int) -> Unit
) {
    var selectedCategory by remember {
        val saved = repository.getLastCategory()
        mutableStateOf(if (saved in CATEGORIES) saved else "全部(2500題.左右移)")
    }
    var searchQuery by remember { mutableStateOf("") }
    var jumpInput by remember { mutableStateOf("") }
    var flashMessage by remember { mutableStateOf<String?>(null) }
    var flashBgColor by remember { mutableStateOf(Color(0xFFD97706)) }
    val coroutineScope = rememberCoroutineScope()
    var isBookmarkLoading by remember { mutableStateOf(false) }

    LaunchedEffect(selectedCategory) {
        repository.setLastCategory(selectedCategory)
    }

    LaunchedEffect(flashMessage) {
        if (flashMessage != null) {
            kotlinx.coroutines.delay(2000L)
            flashMessage = null
        }
    }

    val filteredList = remember(selectedCategory, searchQuery) {
        repository.filterItems(selectedCategory, searchQuery)
    }

    val currentItem = remember(currentId, filteredList) {
        filteredList.firstOrNull { it.id == currentId }
            ?: filteredList.firstOrNull()
            ?: repository.getItem(currentId)
    }

    val isBookmarked = repository.isBookmarked(currentItem.id)

    val currentPos = remember(currentItem, filteredList) {
        val idx = filteredList.indexOfFirst { it.id == currentItem.id }
        if (idx >= 0) idx + 1 else currentItem.id
    }

    val context = LocalContext.current
    val view = LocalView.current
    val keyboardController = LocalSoftwareKeyboardController.current
    val focusManager = LocalFocusManager.current

    fun dismissKeyboard() {
        focusManager.clearFocus(force = true)
        keyboardController?.hide()
        try {
            val imm = context.getSystemService(Context.INPUT_METHOD_SERVICE) as? InputMethodManager
            imm?.hideSoftInputFromWindow(view.windowToken, 0)
            imm?.hideSoftInputFromWindow(view.applicationWindowToken, 0)
            view.clearFocus()
            val activity = context as? Activity
            if (activity != null) {
                WindowCompat.getInsetsController(activity.window, activity.window.decorView)
                    .hide(WindowInsetsCompat.Type.ime())
                activity.currentFocus?.clearFocus()
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    // Navigation logic that never freezes when filtered or jumped
    fun gotoNextLesson() {
        dismissKeyboard()
        if (filteredList.size > 1) {
            val curIdx = filteredList.indexOfFirst { it.id == currentItem.id }
            val nextIdx = if (curIdx >= 0 && curIdx < filteredList.size - 1) curIdx + 1 else 0
            onIdChanged(filteredList[nextIdx].id)
        } else {
            // When filteredList has only 1 match or user wants to continue reading:
            // reset search/filter and advance smoothly in the full 2500 corpus
            searchQuery = ""
            selectedCategory = "全部(2500題.左右移)"
            val nextId = (currentItem.id % repository.getTotalCount()) + 1
            onIdChanged(nextId)
        }
    }

    fun gotoPrevLesson() {
        dismissKeyboard()
        if (filteredList.size > 1) {
            val curIdx = filteredList.indexOfFirst { it.id == currentItem.id }
            val prevIdx = if (curIdx > 0) curIdx - 1 else filteredList.size - 1
            onIdChanged(filteredList[prevIdx].id)
        } else {
            searchQuery = ""
            selectedCategory = "全部(2500題.左右移)"
            val prevId = if (currentItem.id > 1) currentItem.id - 1 else repository.getTotalCount()
            onIdChanged(prevId)
        }
    }

    fun gotoRandomLesson() {
        dismissKeyboard()
        if (filteredList.size > 1) {
            val others = filteredList.filter { it.id != currentItem.id }
            val target = if (others.isNotEmpty()) others.random() else filteredList.random()
            onIdChanged(target.id)
        } else {
            searchQuery = ""
            selectedCategory = "全部(2500題.左右移)"
            var randId = (1..repository.getTotalCount()).random()
            if (randId == currentItem.id && repository.getTotalCount() > 1) {
                randId = (randId % repository.getTotalCount()) + 1
            }
            onIdChanged(randId)
        }
    }

    fun jumpToLessonNumber(rawText: String) {
        dismissKeyboard()
        val n = rawText.trim().toIntOrNull()
        if (n != null && n in 1..repository.getTotalCount()) {
            selectedCategory = "全部(2500題.左右移)"
            searchQuery = ""
            onIdChanged(n)
            jumpInput = ""
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF0B0F19))
    ) {
        // 1. Filter & Search Controls (Compact Height, Tight Spacing)
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xFF131B2E))
                .padding(horizontal = 8.dp, vertical = 4.dp)
        ) {
            // Category Chips Row (Tight theme spacing)
            LazyRow(
                horizontalArrangement = Arrangement.spacedBy(2.5.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                items(CATEGORIES) { cat ->
                    val isSelected = (cat == selectedCategory)
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(8.dp))
                            .background(if (isSelected) Color(0xFF3B82F6) else Color(0xFF1E293B))
                            .clickable {
                                dismissKeyboard()
                                selectedCategory = cat
                                val newMatches = repository.filterItems(cat, searchQuery)
                                if (newMatches.isNotEmpty()) {
                                    onIdChanged(newMatches.first().id)
                                }
                            }
                            .padding(horizontal = 5.dp, vertical = 3.dp)
                    ) {
                        Text(
                            text = cat,
                            fontSize = 11.sp,
                            fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
                            color = if (isSelected) Color.White else Color(0xFFCBD5E1)
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(4.dp))

            // Search Bar + Jump Box Row (Compact 36dp, Text 100% visible, No clipping)
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Compact Search Input
                BasicTextField(
                    value = searchQuery,
                    onValueChange = {
                        searchQuery = it
                        val newMatches = repository.filterItems(selectedCategory, it)
                        if (newMatches.isNotEmpty()) {
                            onIdChanged(newMatches.first().id)
                        }
                    },
                    modifier = Modifier
                        .weight(1f)
                        .height(36.dp)
                        .clip(RoundedCornerShape(8.dp))
                        .background(Color(0xFF1E293B))
                        .padding(horizontal = 8.dp),
                    singleLine = true,
                    textStyle = TextStyle(
                        color = Color.White,
                        fontSize = 12.5.sp,
                        fontWeight = FontWeight.Normal
                    ),
                    cursorBrush = SolidColor(Color(0xFF38BDF8)),
                    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                    keyboardActions = KeyboardActions(onSearch = { dismissKeyboard() }),
                    decorationBox = { innerTextField ->
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.fillMaxSize()
                        ) {
                            Text("🔍 ", fontSize = 11.sp, color = Color(0xFF64748B))
                            Box(modifier = Modifier.weight(1f)) {
                                if (searchQuery.isEmpty()) {
                                    Text("搜尋關鍵字...", fontSize = 12.sp, color = Color(0xFF64748B))
                                }
                                innerTextField()
                            }
                            if (searchQuery.isNotEmpty()) {
                                Text(
                                    text = "✕",
                                    fontSize = 13.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = Color(0xFF94A3B8),
                                    modifier = Modifier
                                        .clickable {
                                            searchQuery = ""
                                            dismissKeyboard()
                                        }
                                        .padding(horizontal = 4.dp)
                                )
                            }
                        }
                    }
                )

                Spacer(modifier = Modifier.width(6.dp))

                // Jump to Lesson Entry (Compact 36dp, 58dp wide)
                BasicTextField(
                    value = jumpInput,
                    onValueChange = { jumpInput = it },
                    modifier = Modifier
                        .width(58.dp)
                        .height(36.dp)
                        .clip(RoundedCornerShape(8.dp))
                        .background(Color(0xFF1E293B))
                        .padding(horizontal = 6.dp),
                    singleLine = true,
                    textStyle = TextStyle(
                        color = Color.White,
                        fontSize = 12.5.sp,
                        fontWeight = FontWeight.Bold
                    ),
                    cursorBrush = SolidColor(Color(0xFF38BDF8)),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number, imeAction = ImeAction.Go),
                    keyboardActions = KeyboardActions(onGo = { jumpToLessonNumber(jumpInput) }),
                    decorationBox = { innerTextField ->
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.fillMaxSize()
                        ) {
                            Box(modifier = Modifier.weight(1f)) {
                                if (jumpInput.isEmpty()) {
                                    Text("題號", fontSize = 11.sp, color = Color(0xFF64748B))
                                }
                                innerTextField()
                            }
                        }
                    }
                )

                Spacer(modifier = Modifier.width(5.dp))

                Button(
                    onClick = { jumpToLessonNumber(jumpInput) },
                    modifier = Modifier.height(36.dp),
                    shape = RoundedCornerShape(8.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2563EB)),
                    contentPadding = PaddingValues(horizontal = 10.dp, vertical = 0.dp)
                ) {
                    Text("前往", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }

                Spacer(modifier = Modifier.width(4.dp))

                // Direct Close Keyboard Button (One tap to dismiss IME anytime)
                Button(
                    onClick = { dismissKeyboard() },
                    modifier = Modifier.height(36.dp),
                    shape = RoundedCornerShape(8.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF334155)),
                    contentPadding = PaddingValues(horizontal = 8.dp, vertical = 0.dp)
                ) {
                    Text("⌨✕", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = Color(0xFFE2E8F0))
                }
            }
        }

        // 2. Scrollable Textbook Card (Tight Spacing, No excessive blank space)
        Column(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null
                ) {
                    dismissKeyboard()
                }
                .padding(horizontal = 8.dp, vertical = 4.dp)
        ) {
            // 2-Second Flash Notification Banner ("閃一下 2秒")
            if (flashMessage != null) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 6.dp)
                        .clip(RoundedCornerShape(8.dp))
                        .background(flashBgColor)
                        .padding(horizontal = 12.dp, vertical = 6.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = flashMessage ?: "",
                        color = Color.White,
                        fontWeight = FontWeight.Bold,
                        fontSize = 12.5.sp
                    )
                }
            }

            // Main Card
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF131B2E)),
                border = CardDefaults.outlinedCardBorder().copy(brush = SolidColor(Color(0xFF1E293B)))
            ) {
                Column(modifier = Modifier.padding(horizontal = 10.dp, vertical = 8.dp)) {

                    // Standalone Lesson Counter Row
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "第 $currentPos / ${filteredList.size} 課 (#${currentItem.id})",
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF38BDF8)
                        )
                    }

                    Spacer(modifier = Modifier.height(3.dp))

                    // Badge Row: Category + Word Count + Status Badges (收藏, 掌握)
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "[${currentItem.category}]",
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFFA5B4FC),
                            modifier = Modifier
                                .background(Color(0xFF312E81), RoundedCornerShape(4.dp))
                                .padding(horizontal = 6.dp, vertical = 2.dp)
                        )
                        Text(
                            text = "[${currentItem.wordCount}字]",
                            fontSize = 11.sp,
                            color = Color(0xFF94A3B8),
                            modifier = Modifier
                                .background(Color(0xFF1E293B), RoundedCornerShape(4.dp))
                                .padding(horizontal = 6.dp, vertical = 2.dp)
                        )
                        if (isBookmarked) {
                            Text(
                                text = "★ 收藏",
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFFFEF08A),
                                modifier = Modifier
                                    .background(Color(0xFF854D0E), RoundedCornerShape(4.dp))
                                    .padding(horizontal = 6.dp, vertical = 2.dp)
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(6.dp))

                    // English Headline
                    Text(
                        text = currentItem.en,
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White,
                        lineHeight = 28.sp
                    )

                    Spacer(modifier = Modifier.height(4.dp))

                    // Pronunciation and Bookmark Row
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Button(
                            onClick = {
                                dismissKeyboard()
                                ttsManager.speak(currentItem.en, slow = false)
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2563EB)),
                            shape = RoundedCornerShape(6.dp),
                            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 4.dp),
                            modifier = Modifier.height(32.dp)
                        ) {
                            Text("🔊 朗讀發音", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                        }

                        Button(
                            onClick = {
                                if (!isBookmarkLoading) {
                                    dismissKeyboard()
                                    coroutineScope.launch {
                                        isBookmarkLoading = true
                                        kotlinx.coroutines.delay(350L) // loading 動態轉圈效果
                                        val willBeBookmarked = !isBookmarked
                                        repository.toggleBookmark(currentItem.id)
                                        isBookmarkLoading = false
                                        flashBgColor = if (willBeBookmarked) Color(0xFFD97706) else Color(0xFF475569)
                                        flashMessage = if (willBeBookmarked)
                                            "⭐ 已加入收藏！(可於頂端「各種標記」查看)"
                                        else
                                            "已取消收藏！"
                                    }
                                }
                            },
                            enabled = !isBookmarkLoading,
                            colors = ButtonDefaults.buttonColors(
                                containerColor = if (isBookmarked) Color(0xFFB45309) else Color(0xFF1E293B)
                            ),
                            shape = RoundedCornerShape(6.dp),
                            modifier = Modifier.height(32.dp),
                            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 4.dp)
                        ) {
                            if (isBookmarkLoading) {
                                CircularProgressIndicator(
                                    modifier = Modifier.size(13.dp),
                                    strokeWidth = 2.dp,
                                    color = Color(0xFFFDE68A)
                                )
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(
                                    text = "處理中...",
                                    fontSize = 11.sp,
                                    color = Color(0xFFFDE68A)
                                )
                            } else {
                                Text(
                                    text = if (isBookmarked) "★ 已收藏" else "⭐ 收藏",
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (isBookmarked) Color(0xFFFDE68A) else Color(0xFFCBD5E1)
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(6.dp))

                    // Traditional Chinese Card
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(8.dp))
                            .background(Color(0xFF172554))
                            .border(1.dp, Color(0xFF1E40AF), RoundedCornerShape(8.dp))
                            .padding(horizontal = 10.dp, vertical = 6.dp)
                    ) {
                        Column {
                            Text(
                                text = "🈯 道地核心釋義",
                                fontSize = 10.5.sp,
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFF93C5FD)
                            )
                            Spacer(modifier = Modifier.height(2.dp))
                            Text(
                                text = currentItem.zh,
                                fontSize = 16.sp,
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFFDBEAFE)
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(5.dp))

                    // Dialogue Scenario Card
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(8.dp))
                            .background(Color(0xFF0F172A))
                            .border(1.dp, Color(0xFF1E293B), RoundedCornerShape(8.dp))
                            .padding(horizontal = 10.dp, vertical = 6.dp)
                    ) {
                        Column {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = "💬 經典生活對話示範",
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = Color(0xFF38BDF8)
                                )

                                Button(
                                    onClick = {
                                        dismissKeyboard()
                                        ttsManager.speakDialogue(currentItem.spkA, currentItem.spkB)
                                    },
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0284C7)),
                                    shape = RoundedCornerShape(6.dp),
                                    contentPadding = PaddingValues(horizontal = 8.dp, vertical = 0.dp),
                                    modifier = Modifier.height(26.dp)
                                ) {
                                    Text("🔊 朗讀對話", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color.White)
                                }
                            }
                            Spacer(modifier = Modifier.height(3.dp))
                            Text(
                                text = currentItem.spkA,
                                fontSize = 13.sp,
                                color = Color(0xFFCBD5E1),
                                lineHeight = 17.sp
                            )
                            if (currentItem.spkAZh.isNotBlank()) {
                                Text(
                                    text = if (currentItem.spkAZh.startsWith("（") || currentItem.spkAZh.startsWith("(")) currentItem.spkAZh else "（${currentItem.spkAZh}）",
                                    fontSize = 11.5.sp,
                                    color = Color(0xFF94A3B8),
                                    lineHeight = 15.sp,
                                    modifier = Modifier.padding(start = 4.dp, top = 1.dp, bottom = 4.dp)
                                )
                            }
                            Spacer(modifier = Modifier.height(2.dp))
                            Text(
                                text = currentItem.spkB,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFF60A5FA),
                                lineHeight = 17.sp
                            )
                            if (currentItem.spkBZh.isNotBlank()) {
                                Text(
                                    text = if (currentItem.spkBZh.startsWith("（") || currentItem.spkBZh.startsWith("(")) currentItem.spkBZh else "（${currentItem.spkBZh}）",
                                    fontSize = 11.5.sp,
                                    fontWeight = FontWeight.Medium,
                                    color = Color(0xFF93C5FD),
                                    lineHeight = 15.sp,
                                    modifier = Modifier.padding(start = 4.dp, top = 1.dp)
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(5.dp))

                    // Cultural Nuance & Usage Notes Card
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(8.dp))
                            .background(Color(0xFF0F172A))
                            .border(1.dp, Color(0xFF1E293B), RoundedCornerShape(8.dp))
                            .padding(horizontal = 10.dp, vertical = 6.dp)
                    ) {
                        Column {
                            Text(
                                text = "💡 母語思維與深度解析",
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFFFBBF24)
                            )
                            Spacer(modifier = Modifier.height(3.dp))
                            Text(
                                text = currentItem.note,
                                fontSize = 12.sp,
                                color = Color(0xFF94A3B8),
                                lineHeight = 16.sp
                            )
                        }
                    }
                }
            }
        }

        // 3. Bottom Navigation Bar: 上一課, 隨機, 下一課 GUARANTEED IN THE SAME ROW
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xFF0F172A))
                .padding(horizontal = 8.dp, vertical = 4.dp),
            horizontalArrangement = Arrangement.spacedBy(6.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Button(
                onClick = { gotoPrevLesson() },
                modifier = Modifier
                    .weight(1f)
                    .height(38.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF334155)),
                shape = RoundedCornerShape(8.dp),
                contentPadding = PaddingValues(horizontal = 2.dp, vertical = 0.dp)
            ) {
                Text("◀ 上一課", fontSize = 12.5.sp, fontWeight = FontWeight.Bold, maxLines = 1)
            }

            Button(
                onClick = { gotoRandomLesson() },
                modifier = Modifier
                    .weight(1f)
                    .height(38.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF7C3AED)),
                shape = RoundedCornerShape(8.dp),
                contentPadding = PaddingValues(horizontal = 2.dp, vertical = 0.dp)
            ) {
                Text("🎲 隨機", fontSize = 12.5.sp, fontWeight = FontWeight.Bold, maxLines = 1)
            }

            Button(
                onClick = { gotoNextLesson() },
                modifier = Modifier
                    .weight(1f)
                    .height(38.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2563EB)),
                shape = RoundedCornerShape(8.dp),
                contentPadding = PaddingValues(horizontal = 2.dp, vertical = 0.dp)
            ) {
                Text("下一課 ▶", fontSize = 12.5.sp, fontWeight = FontWeight.Bold, maxLines = 1)
            }
        }
    }
}
