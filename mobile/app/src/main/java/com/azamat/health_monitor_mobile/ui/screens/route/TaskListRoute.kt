package com.azamat.health_monitor_mobile.ui.screens.route

import android.util.Log
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import com.azamat.health_monitor_mobile.domain.model.TaskDomain
import com.azamat.health_monitor_mobile.ui.screens.TaskListScreen
import com.azamat.health_monitor_mobile.ui.viewmodel.TaskViewModel

@Composable
fun TaskListRoute(
    viewModel: TaskViewModel = hiltViewModel(),
    onTaskClick: (TaskDomain) -> Unit
){
    val openTasks by viewModel.openTasks.collectAsState()
    val doneTasks by viewModel.doneTasks.collectAsState()

    TaskListScreen(
        openTasks = openTasks,
        doneTasks = doneTasks,
        onTaskClick = onTaskClick
    )
}