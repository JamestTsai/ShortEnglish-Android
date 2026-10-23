# ProGuard / R8 Rules for JpnCrosswordPuzzle

# Retain line numbers for crash reporting on Google Play Console
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile

# AdMob
-keep class com.google.android.gms.ads.** { *; }
-keep interface com.google.android.gms.ads.** { *; }

# Data classes
-keep class com.example.jpncrosswordpuzzle.data.** { *; }
-keepclassmembers class com.example.jpncrosswordpuzzle.data.** { *; }

# Audio and TTS helpers
-keep class com.example.jpncrosswordpuzzle.sound.** { *; }

# Compose & Coroutines warnings suppression
-dontwarn androidx.compose.**
-dontwarn kotlinx.coroutines.**
