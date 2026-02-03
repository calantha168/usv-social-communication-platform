#!/usr/bin/env Rscript

# =========================
# 00_setup.R
# Project 2 — R Analysis Layer
# Purpose: reproducible setup for all downstream scripts
# Experimental unit: SESSION (dyadic interaction)
# =========================

source("analysis/r/00_setup.R")
PATHS <- readRDS(file.path("results/logs/paths.rds"))

# ---------- Reproducibility ----------
set.seed(20260203)  # fixed seed for any resampling/bootstrap later
options(stringsAsFactors = FALSE)
options(dplyr.summarise.inform = FALSE)

# ---------- Project root + paths ----------
# We assume this script is executed from the repo root:
#   Rscript analysis/r/00_setup.R
# If run from elsewhere, we'll fall back to locating the root by walking upward.
suppressWarnings(suppressMessages({
  library(here)
}))

find_project_root <- function() {
  # Try 'here' first (works if .here exists or Rproj is present)
  root <- tryCatch(here::here(), error = function(e) NA_character_)
  if (!is.na(root) && dir.exists(root)) return(normalizePath(root))

  # Fallback: walk up from current working directory looking for key folders
  wd <- normalizePath(getwd())
  candidates <- c("analysis", "data", "project_2_statistical_engine")
  cur <- wd

  for (i in 1:8) {
    ok <- all(file.exists(file.path(cur, c("analysis", "data"))))
    if (ok) return(cur)
    parent <- dirname(cur)
    if (parent == cur) break
    cur <- parent
  }

  # If nothing found, assume current directory is root
  wd
}

ROOT <- find_project_root()

PATHS <- list(
  root      = ROOT,
  analysis  = file.path(ROOT, "analysis", "r"),
  helpers   = file.path(ROOT, "analysis", "r", "helpers"),
  data      = file.path(ROOT, "data"),
  derived   = file.path(ROOT, "data", "derived"),
  results   = file.path(ROOT, "results"),
  tables    = file.path(ROOT, "results", "tables"),
  figures   = file.path(ROOT, "results", "figures"),
  logs      = file.path(ROOT, "results", "logs")
)

# ---------- Create required directories ----------
dir.create(PATHS$derived, recursive = TRUE, showWarnings = FALSE)
dir.create(PATHS$tables,  recursive = TRUE, showWarnings = FALSE)
dir.create(PATHS$figures, recursive = TRUE, showWarnings = FALSE)
dir.create(PATHS$logs,    recursive = TRUE, showWarnings = FALSE)

# ---------- Package management ----------
# Keep this list tight + explicit so runs are stable.
required_pkgs <- c(
  "tidyverse",    # dplyr, ggplot2, readr, tibble, tidyr
  "janitor",      # clean_names, tabyl
  "rstatix",      # easy Welch tests, nonparametric tests, effect sizes
  "effectsize",   # standardized effect sizes + CIs
  "FSA",          # Dunn test (Kruskal-Wallis posthoc)
  "DescTools",    # winsorize if needed later
  "performance",  # model diagnostics (useful for NB models)
  "glmmTMB",      # negative binomial regression (session-level)
  "broom",        # tidy model outputs
  "broom.mixed"   # tidy mixed/GLMM outputs
)

install_if_missing <- function(pkgs) {
  missing <- pkgs[!pkgs %in% rownames(installed.packages())]
  if (length(missing) > 0) {
    message("Installing missing packages: ", paste(missing, collapse = ", "))
    install.packages(missing, repos = "https://cloud.r-project.org")
  }
}

install_if_missing(required_pkgs)

suppressPackageStartupMessages({
  library(tidyverse)
  library(janitor)
  library(rstatix)
  library(effectsize)
  library(FSA)
  library(DescTools)
  library(performance)
  library(glmmTMB)
  library(broom)
  library(broom.mixed)
})

# ---------- Helper sourcing ----------
stats_utils_path <- file.path(PATHS$helpers, "stats_utils.R")
plot_utils_path  <- file.path(PATHS$helpers, "plotting_utils.R")

if (!file.exists(stats_utils_path)) {
  warning("Missing helper: ", stats_utils_path, call. = FALSE)
} else {
  source(stats_utils_path)
}

if (!file.exists(plot_utils_path)) {
  warning("Missing helper: ", plot_utils_path, call. = FALSE)
} else {
  source(plot_utils_path)
}

# ---------- Global ggplot defaults (minimal + consistent) ----------
theme_set(theme_minimal(base_size = 12))

# ---------- Standard write helpers ----------
# Use these in downstream scripts to avoid inconsistent file naming.
timestamp_string <- function() format(Sys.time(), "%Y-%m-%d_%H-%M-%S")

write_run_manifest <- function() {
  manifest <- tibble::tibble(
    run_timestamp = as.character(Sys.time()),
    root          = PATHS$root,
    r_version     = paste(R.version$major, R.version$minor, sep = "."),
    platform      = R.version$platform,
    packages      = paste(required_pkgs, collapse = ", ")
  )

  out <- file.path(PATHS$logs, paste0("run_manifest_", timestamp_string(), ".csv"))
  readr::write_csv(manifest, out)
  invisible(out)
}

manifest_file <- write_run_manifest()

# ---------- Print key info ----------
message(" Project 2 R setup complete.")
message("Root:   ", PATHS$root)
message("Derived:", PATHS$derived)
message("Results:", PATHS$results)
message("Manifest saved: ", manifest_file)

# ---------- Export PATHS for downstream scripts ----------
# When scripts are called via Rscript, global variables won't persist across separate runs,
# so downstream scripts should either:
#   1) source 00_setup.R (recommended), or
#   2) re-create PATHS similarly.
#
# We also save paths to a small RDS for convenience.
saveRDS(PATHS, file.path(PATHS$logs, "paths.rds"))

