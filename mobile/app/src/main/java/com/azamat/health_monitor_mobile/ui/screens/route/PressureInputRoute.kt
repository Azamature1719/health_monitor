package com.azamat.health_monitor_mobile.ui.screens.route

import android.util.Log
import androidx.compose.runtime.Composable
import androidx.hilt.navigation.compose.hiltViewModel
import com.azamat.health_monitor_mobile.ui.screens.PressureInputScreen
import com.azamat.health_monitor_mobile.ui.viewmodel.ManualInputViewModel

@Composable
fun PressureInputRoute(
    taskId: Int,
    onSubmit: () -> Unit
) {
    Log.d("PressureInputRoute", "PressureInputRoute вызван для taskId=$taskId")
    val viewModel: ManualInputViewModel = hiltViewModel()

    PressureInputScreen(
        onSubmit = { pressure ->
            viewModel.submitResult(taskId, pressure)
            onSubmit()
        }
    )
}