package com.azamat.health_monitor_mobile.ui.screens

import androidx.compose.runtime.Composable
import androidx.hilt.navigation.compose.hiltViewModel
import com.azamat.health_monitor_mobile.ui.viewmodel.OrderViewModel
import androidx.lifecycle.viewmodel.compose.viewModel

@Composable
fun OrderScreen(
) {
    val viewModel: OrderViewModel = hiltViewModel()
}