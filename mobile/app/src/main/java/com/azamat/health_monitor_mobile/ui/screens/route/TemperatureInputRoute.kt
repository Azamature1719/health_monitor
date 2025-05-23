package com.azamat.health_monitor_mobile.ui.screens.route

import android.util.Log
import androidx.compose.runtime.Composable
import androidx.hilt.navigation.compose.hiltViewModel
import com.azamat.health_monitor_mobile.ui.viewmodel.ManualInputViewModel
import com.azamat.health_monitor_mobile.ui.screens.TemperatureInputScreen

@Composable
fun TemperatureInputRoute(
    taskId: Int,
    onSubmit: () -> Unit
) {
    Log.d("TemperatureInputRoute", "TemperatureInputRoute вызван для taskId=$taskId")
    val viewModel: ManualInputViewModel = hiltViewModel()

    TemperatureInputScreen(
        onSubmit = { temperature ->
            viewModel.submitResult(taskId, temperature)
            onSubmit()
        }
    )
}