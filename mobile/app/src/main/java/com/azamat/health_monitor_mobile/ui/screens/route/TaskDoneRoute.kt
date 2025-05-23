package com.azamat.health_monitor_mobile.ui.screens.route

import android.util.Log
import androidx.compose.runtime.Composable
import com.azamat.health_monitor_mobile.ui.screens.TaskDoneScreen

@Composable
fun TaskDoneRoute(
    taskId: Int,
    onSubmit: () -> Unit
) {
    Log.d("TaskDoneRoute", "TaskDoneRoute вызван")
    TaskDoneScreen(
        onSubmit = onSubmit
    )
}