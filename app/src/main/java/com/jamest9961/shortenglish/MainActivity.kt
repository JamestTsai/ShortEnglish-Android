package com.jamest9961.shortenglish

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import com.google.android.gms.ads.MobileAds
import com.jamest9961.shortenglish.data.SentenceRepository
import com.jamest9961.shortenglish.sound.TtsManager
import com.jamest9961.shortenglish.ui.MainScreen

class MainActivity : ComponentActivity() {

    private lateinit var repository: SentenceRepository
    private lateinit var ttsManager: TtsManager

    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)

        try {
            MobileAds.initialize(this) {}
        } catch (e: Exception) {
            e.printStackTrace()
        }

        repository = SentenceRepository(applicationContext)
        ttsManager = TtsManager(this)

        setContent {
            Surface(
                modifier = Modifier
                    .fillMaxSize()
                    .safeDrawingPadding(),
                color = Color(0xFF0B0F19)
            ) {
                MainScreen(
                    repository = repository,
                    ttsManager = ttsManager
                )
            }
        }
    }

    override fun onStop() {
        super.onStop()
        ttsManager.stop()
    }

    override fun onDestroy() {
        super.onDestroy()
        ttsManager.shutdown()
    }
}
