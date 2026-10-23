package com.jamest9961.shortenglish.ui

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.jamest9961.shortenglish.R

enum class AppTab(val label: String) {
    TEXTBOOK("📖 課本研讀"),
    QUIZ_EN("測驗(英)"),
    QUIZ_ZH("測驗(中)"),
    NOTEBOOK("各種標記")
}

@Composable
fun TopNavBar(
    currentTab: AppTab,
    onTabSelected: (AppTab) -> Unit,
    bookmarkedCount: Int,
    wrongCount: Int
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color(0xFF0F172A))
            .padding(top = 6.dp, bottom = 4.dp, start = 10.dp, end = 10.dp)
    ) {
        // Top Row: In-App Logo + Title + Stats
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            // Logo & Title
            Row(verticalAlignment = Alignment.CenterVertically) {
                Image(
                    painter = painterResource(id = R.drawable.ic_app_logo),
                    contentDescription = "App Logo",
                    modifier = Modifier
                        .size(40.dp)
                        .clip(RoundedCornerShape(8.dp))
                        .border(1.dp, Color(0xFFFACC15), RoundedCornerShape(8.dp))
                )
                Spacer(modifier = Modifier.width(8.dp))
                Column {
                    Text(
                        text = "道地英語短句2500",
                        fontSize = 17.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                    Text(
                        text = "2500 核心短句 (6單字以內)",
                        fontSize = 10.5.sp,
                        color = Color(0xFF94A3B8)
                    )
                }
            }

            // Stats Badges
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = "⭐ $bookmarkedCount | ❌ $wrongCount",
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFFCBD5E1),
                    modifier = Modifier
                        .background(Color(0xFF1E293B), RoundedCornerShape(6.dp))
                        .padding(horizontal = 8.dp, vertical = 3.dp)
                )
            }
        }

        Spacer(modifier = Modifier.height(6.dp))

        // Mode Segmented Buttons: 4 compact buttons (各種標記縮小)
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            AppTab.values().forEach { tab ->
                val isSelected = (tab == currentTab)
                val isNotebook = (tab == AppTab.NOTEBOOK)
                val tabWeight = if (isNotebook) 0.85f else 1f

                val bgColor = if (isSelected) {
                    if (isNotebook) Color(0xFF7F1D1D) else Color(0xFF2563EB)
                } else {
                    Color(0xFF1E293B)
                }

                val textColor = if (isSelected) {
                    if (isNotebook) Color(0xFFFEE2E2) else Color.White
                } else {
                    if (isNotebook) Color(0xFFEF4444) else Color(0xFF94A3B8)
                }

                val borderColor = if (isNotebook) {
                    if (isSelected) Color(0xFFEF4444) else Color(0xFF991B1B)
                } else {
                    Color.Transparent
                }

                Box(
                    modifier = Modifier
                        .weight(tabWeight)
                        .height(35.dp)
                        .clip(RoundedCornerShape(8.dp))
                        .background(bgColor)
                        .border(1.dp, borderColor, RoundedCornerShape(8.dp))
                        .clickable { onTabSelected(tab) },
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = tab.label,
                        fontSize = if (isNotebook) 10.sp else 11.5.sp,
                        fontWeight = if (isSelected || isNotebook) FontWeight.Bold else FontWeight.Medium,
                        color = textColor,
                        maxLines = 1
                    )
                }
            }
        }
    }
}
