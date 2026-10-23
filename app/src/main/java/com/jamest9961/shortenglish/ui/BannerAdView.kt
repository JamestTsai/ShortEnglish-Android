package com.jamest9961.shortenglish.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import com.google.android.gms.ads.AdListener
import com.google.android.gms.ads.AdRequest
import com.google.android.gms.ads.AdSize
import com.google.android.gms.ads.AdView
import com.google.android.gms.ads.LoadAdError

@Composable
fun BottomTestBannerAdView(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .fillMaxWidth()
            .background(Color(0xFF0F172A))
            .border(width = 0.5.dp, color = Color(0xFF334155)),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "贊助商廣告 (點擊支持開發者)",
            fontSize = 9.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF94A3B8),
            modifier = Modifier.padding(top = 2.dp, bottom = 1.dp)
        )

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(50.dp),
            contentAlignment = Alignment.Center
        ) {
            AndroidView(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp),
                factory = { context ->
                    try {
                        AdView(context).apply {
                            setAdSize(AdSize.BANNER)
                            // Google AdMob 正式橫幅廣告單元 ID
                            adUnitId = "ca-app-pub-2094200238362964/4442679947"
                            adListener = object : AdListener() {
                                override fun onAdFailedToLoad(loadAdError: LoadAdError) {
                                    super.onAdFailedToLoad(loadAdError)
                                }
                            }
                            loadAd(AdRequest.Builder().build())
                        }
                    } catch (e: Exception) {
                        e.printStackTrace()
                        android.view.View(context)
                    }
                }
            )
        }
    }
}
