package com.jamest9961.shortenglish.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import com.jamest9961.shortenglish.data.QuizType
import com.jamest9961.shortenglish.data.SentenceRepository
import com.jamest9961.shortenglish.sound.TtsManager

@Composable
fun MainScreen(
    repository: SentenceRepository,
    ttsManager: TtsManager
) {
    var currentTab by remember {
        val savedName = repository.getLastTabName()
        val initialTab = try {
            AppTab.valueOf(savedName)
        } catch (e: Exception) {
            AppTab.TEXTBOOK
        }
        mutableStateOf(initialTab)
    }

    var currentTextbookId by remember {
        mutableStateOf(repository.getLastTextbookId())
    }

    LaunchedEffect(currentTab) {
        repository.setLastTabName(currentTab.name)
    }

    LaunchedEffect(currentTextbookId) {
        repository.setLastTextbookId(currentTextbookId)
    }

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        topBar = {
            TopNavBar(
                currentTab = currentTab,
                onTabSelected = { currentTab = it },
                bookmarkedCount = repository.getBookmarkedIds().size,
                wrongCount = (repository.getWrongIdsMode1() + repository.getWrongIdsMode2()).size
            )
        },
        bottomBar = {
            // Google AdMob 官方測試橫幅廣告（固定置於最下方）
            BottomTestBannerAdView(modifier = Modifier.fillMaxWidth())
        },
        containerColor = Color(0xFF0B0F19)
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            when (currentTab) {
                AppTab.TEXTBOOK -> {
                    TextbookScreen(
                        repository = repository,
                        ttsManager = ttsManager,
                        currentId = currentTextbookId,
                        onIdChanged = {
                            currentTextbookId = it
                            repository.setLastTextbookId(it)
                        }
                    )
                }
                AppTab.QUIZ_EN -> {
                    QuizScreen(
                        initialQuizType = QuizType.EN_TO_ZH,
                        repository = repository,
                        ttsManager = ttsManager,
                        onBackToTextbook = { currentTab = AppTab.TEXTBOOK }
                    )
                }
                AppTab.QUIZ_ZH -> {
                    QuizScreen(
                        initialQuizType = QuizType.ZH_TO_EN,
                        repository = repository,
                        ttsManager = ttsManager,
                        onBackToTextbook = { currentTab = AppTab.TEXTBOOK }
                    )
                }
                AppTab.NOTEBOOK -> {
                    NotebookScreen(
                        repository = repository,
                        ttsManager = ttsManager,
                        onBackToTextbook = { currentTab = AppTab.TEXTBOOK },
                        onJumpToTextbook = { targetId ->
                            currentTextbookId = targetId
                            currentTab = AppTab.TEXTBOOK
                        }
                    )
                }
            }
        }
    }
}
