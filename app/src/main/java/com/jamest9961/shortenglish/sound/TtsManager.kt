package com.jamest9961.shortenglish.sound

import android.content.Context
import android.speech.tts.TextToSpeech
import java.util.Locale

class TtsManager(context: Context) : TextToSpeech.OnInitListener {

    private var tts: TextToSpeech? = TextToSpeech(context.applicationContext, this)
    private var isReady = false

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            val result = tts?.setLanguage(Locale.US)
            if (result != TextToSpeech.LANG_MISSING_DATA && result != TextToSpeech.LANG_NOT_SUPPORTED) {
                isReady = true
            }
        }
    }

    fun speak(text: String, slow: Boolean = false) {
        if (!isReady || tts == null) return
        try {
            tts?.setSpeechRate(if (slow) 0.75f else 1.0f)
            tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "ShortEnglishTts")
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun speakDialogue(spkA: String, spkB: String, slow: Boolean = false) {
        if (!isReady || tts == null) return
        try {
            var textA = if (spkA.contains(":")) spkA.substringAfter(":").trim() else spkA
            var textB = if (spkB.contains(":")) spkB.substringAfter(":").trim() else spkB
            textA = textA.substringBefore("\n").trim()
            textB = textB.substringBefore("\n").trim()

            tts?.setSpeechRate(if (slow) 0.75f else 1.0f)
            tts?.speak(textA, TextToSpeech.QUEUE_FLUSH, null, "ShortEnglishTts_A")
            tts?.playSilentUtterance(400L, TextToSpeech.QUEUE_ADD, "ShortEnglishTts_Pause")
            tts?.speak(textB, TextToSpeech.QUEUE_ADD, null, "ShortEnglishTts_B")
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun stop() {
        try {
            tts?.stop()
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun shutdown() {
        try {
            tts?.stop()
            tts?.shutdown()
            tts = null
            isReady = false
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
