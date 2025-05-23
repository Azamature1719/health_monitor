package com.azamat.health_monitor_mobile.ui.screens.route

import android.util.Log
import androidx.compose.runtime.Composable
import androidx.hilt.navigation.compose.hiltViewModel
import com.azamat.health_monitor_mobile.ui.screens.MoodInputScreen
import com.azamat.health_monitor_mobile.ui.viewmodel.ManualInputViewModel

@Composable
fun MoodInputRoute(
    taskId: Int,
    onSubmit: () -> Unit
) {
    Log.d("MoodInputRoute", "MoodInputRoute вызван для taskId=$taskId")
    val viewModel: ManualInputViewModel = hiltViewModel()

    MoodInputScreen(
        onSubmit = { mood ->
            viewModel.submitResult(taskId, mood)
            onSubmit()
        }
    )
}