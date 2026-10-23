plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.compose.compiler)
    alias(libs.plugins.kotlin.serialization)
}

android {
    namespace = "com.jamest9961.shortenglish"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.jamest9961.shortenglish"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1.0.0"
    }

    signingConfigs {
        create("release") {
            storeFile = file("release-key.jks")
            storePassword = "jamest9961Grammar"
            keyAlias = "upload"
            keyPassword = "jamest9961Grammar"
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            ndk {
                debugSymbolLevel = "SYMBOL_TABLE"
            }
        }
        debug {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    buildFeatures {
        compose = true
        aidl = false
        buildConfig = false
        shaders = false
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

// 嚴格強制 modern non-vulnerable Fragment 與 WorkManager 版本，防止過時版本警告或閃退
configurations.all {
    resolutionStrategy {
        force("androidx.fragment:fragment:1.8.6")
        force("androidx.fragment:fragment-ktx:1.8.6")
        force("androidx.work:work-runtime:2.9.1")
        force("androidx.work:work-runtime-ktx:2.9.1")
    }
}

kotlin {
    jvmToolchain(17)
}

dependencies {
    val composeBom = platform(libs.androidx.compose.bom)
    implementation(composeBom)
    androidTestImplementation(composeBom)

    // Core Android dependencies
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.activity.compose)

    // Arch Components
    implementation(libs.androidx.lifecycle.runtime.compose)
    implementation(libs.androidx.lifecycle.viewmodel.compose)

    // Compose
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.ui.tooling.preview)
    implementation(libs.androidx.compose.material3)
    debugImplementation(libs.androidx.compose.ui.tooling)

    // Google AdMob SDK
    implementation("com.google.android.gms:play-services-ads:23.6.0")

    // JSON serialization
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.7.3")
}
