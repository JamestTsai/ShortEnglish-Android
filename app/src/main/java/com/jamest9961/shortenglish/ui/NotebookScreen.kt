package com.jamest9961.shortenglish.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.jamest9961.shortenglish.data.SentenceItem
import com.jamest9961.shortenglish.data.SentenceRepository
import com.jamest9961.shortenglish.sound.TtsManager

enum class NotebookTab(val label: String) {
    BOOKMARKS("⭐ 收藏"),
    WRONG("❌ 錯題")
}

@Composable
fun NotebookScreen(
    repository: SentenceRepository,
    ttsManager: TtsManager,
    onBackToTextbook: () -> Unit,
    onJumpToTextbook: (Int) -> Unit
) {
    var selectedTab by remember {
        val saved = repository.getLastNotebookTab()
        val initial = try {
            NotebookTab.valueOf(saved)
        } catch (e: Exception) {
            NotebookTab.BOOKMARKS
        }
        mutableStateOf(initial)
    }
    var refreshKey by remember { mutableStateOf(0) }
    var selectedIds by remember(selectedTab, refreshKey) { mutableStateOf(setOf<Int>()) }

    LaunchedEffect(selectedTab) {
        repository.setLastNotebookTab(selectedTab.name)
    }

    val currentIds = remember(selectedTab, refreshKey) {
        when (selectedTab) {
            NotebookTab.BOOKMARKS -> repository.getBookmarkedIds().sorted()
            NotebookTab.WRONG -> (repository.getWrongIdsMode1() + repository.getWrongIdsMode2()).toSet().sorted()
        }
    }

    val currentItems = remember(currentIds) {
        currentIds.map { repository.getItem(it) }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF0B0F19))
    ) {
        // Sub-tabs Row (2 clean, compact tabs: 收藏 / 錯題)
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xFF131B2E))
                .padding(horizontal = 10.dp, vertical = 4.dp),
            horizontalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            NotebookTab.values().forEach { tab ->
                val isSelected = (tab == selectedTab)
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .clip(RoundedCornerShape(6.dp))
                        .background(if (isSelected) Color(0xFF3B82F6) else Color(0xFF1E293B))
                        .clickable {
                            selectedTab = tab
                            selectedIds = emptySet()
                        }
                        .padding(vertical = 5.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = tab.label,
                        fontSize = 11.sp,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
                        color = if (isSelected) Color.White else Color(0xFF94A3B8)
                    )
                }
            }
        }

        // Header Summary Row with [ ◀ 回到上一階 ] (緊湊上下空白)
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xFF0F172A))
                .padding(horizontal = 10.dp, vertical = 3.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "${selectedTab.label} (共 ${currentItems.size} 筆)",
                fontSize = 11.5.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFFCBD5E1)
            )

            Button(
                onClick = onBackToTextbook,
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF334155)),
                shape = RoundedCornerShape(5.dp),
                contentPadding = PaddingValues(horizontal = 7.dp, vertical = 0.dp),
                modifier = Modifier.height(25.dp)
            ) {
                Text("◀ 回到上一階", fontSize = 10.5.sp, fontWeight = FontWeight.Bold, color = Color.White)
            }
        }

        // Batch Action Bar: Checkbox for Select All + Delete Selected Button
        if (currentItems.isNotEmpty()) {
            val allSelected = selectedIds.size == currentIds.size && currentIds.isNotEmpty()
            val hasSelection = selectedIds.isNotEmpty()

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color(0xFF161F36))
                    .padding(horizontal = 10.dp, vertical = 3.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.clickable {
                        selectedIds = if (allSelected) emptySet() else currentIds.toSet()
                    }
                ) {
                    Checkbox(
                        checked = allSelected,
                        onCheckedChange = { checked ->
                            selectedIds = if (checked) currentIds.toSet() else emptySet()
                        },
                        colors = CheckboxDefaults.colors(
                            checkedColor = Color(0xFF3B82F6),
                            uncheckedColor = Color(0xFF64748B)
                        ),
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = if (allSelected) "取消全選" else "全選",
                        fontSize = 11.5.sp,
                        fontWeight = FontWeight.Medium,
                        color = Color(0xFFE2E8F0)
                    )
                }

                Button(
                    onClick = {
                        if (hasSelection) {
                            when (selectedTab) {
                                NotebookTab.BOOKMARKS -> repository.removeBookmarks(selectedIds)
                                NotebookTab.WRONG -> repository.removeWrongs(selectedIds)
                            }
                            selectedIds = emptySet()
                            refreshKey++
                        }
                    },
                    enabled = hasSelection,
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (hasSelection) Color(0xFFDC2626) else Color(0xFF1E293B),
                        disabledContainerColor = Color(0xFF1E293B)
                    ),
                    shape = RoundedCornerShape(5.dp),
                    contentPadding = PaddingValues(horizontal = 10.dp, vertical = 0.dp),
                    modifier = Modifier.height(27.dp)
                ) {
                    Text(
                        text = if (hasSelection) "🗑 刪除所選 (${selectedIds.size})" else "🗑 勾選刪除",
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        color = if (hasSelection) Color.White else Color(0xFF64748B)
                    )
                }
            }
        }

        // List Content
        if (currentItems.isEmpty()) {
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth(),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "（目前此清單中尚無項目，請在研讀或測驗時加入）",
                    fontSize = 14.sp,
                    color = Color(0xFF64748B)
                )
            }
        } else {
            LazyColumn(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .padding(horizontal = 8.dp, vertical = 4.dp),
                verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                items(currentItems, key = { it.id }) { item ->
                    val isChecked = selectedIds.contains(item.id)
                    NotebookItemRow(
                        item = item,
                        isSelected = isChecked,
                        onToggleSelect = {
                            selectedIds = if (isChecked) {
                                selectedIds - item.id
                            } else {
                                selectedIds + item.id
                            }
                        },
                        onPlayVoice = { ttsManager.speak(item.en) },
                        onStudy = { onJumpToTextbook(item.id) }
                    )
                }
            }
        }
    }
}

@Composable
fun NotebookItemRow(
    item: SentenceItem,
    isSelected: Boolean,
    onToggleSelect: () -> Unit,
    onPlayVoice: () -> Unit,
    onStudy: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onToggleSelect() },
        shape = RoundedCornerShape(8.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (isSelected) Color(0xFF1E293B) else Color(0xFF131B2E)
        ),
        border = CardDefaults.outlinedCardBorder().copy(
            brush = androidx.compose.ui.graphics.SolidColor(
                if (isSelected) Color(0xFF3B82F6) else Color(0xFF1E293B)
            )
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 8.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Checkbox for selection
            Checkbox(
                checked = isSelected,
                onCheckedChange = { onToggleSelect() },
                colors = CheckboxDefaults.colors(
                    checkedColor = Color(0xFF3B82F6),
                    uncheckedColor = Color(0xFF64748B)
                ),
                modifier = Modifier.size(24.dp)
            )

            Spacer(modifier = Modifier.width(6.dp))

            // Index Pill
            Text(
                text = "#${item.id}",
                fontSize = 11.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF38BDF8),
                modifier = Modifier
                    .background(Color(0xFF0F172A), RoundedCornerShape(4.dp))
                    .padding(horizontal = 5.dp, vertical = 2.dp)
            )

            Spacer(modifier = Modifier.width(8.dp))

            // Text Info
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = item.en,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = item.zh,
                    fontSize = 12.5.sp,
                    color = Color(0xFF94A3B8)
                )
            }

            Spacer(modifier = Modifier.width(6.dp))

            // Voice Button
            Button(
                onClick = onPlayVoice,
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2563EB)),
                shape = RoundedCornerShape(5.dp),
                contentPadding = PaddingValues(horizontal = 6.dp, vertical = 0.dp),
                modifier = Modifier.height(28.dp)
            ) {
                Text("🔊", fontSize = 11.sp)
            }

            Spacer(modifier = Modifier.width(4.dp))

            // Study Jump Button
            Button(
                onClick = onStudy,
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF334155)),
                shape = RoundedCornerShape(5.dp),
                contentPadding = PaddingValues(horizontal = 7.dp, vertical = 0.dp),
                modifier = Modifier.height(28.dp)
            ) {
                Text("研讀", fontSize = 11.sp)
            }
        }
    }
}
